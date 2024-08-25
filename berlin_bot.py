import time
import os
import logging
from platform import system as platform_system
from selenium import webdriver
from selenium.webdriver.common.by import By
import winsound

# Перевірка системи
current_platform = platform_system()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Edge
        self._implicit_wait_time = 5

    def __enter__(self) -> webdriver.Edge:
        logging.info("Opening browser")
        options = webdriver.EdgeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Edge(options=options)
        self._driver.implicitly_wait(self._implicit_wait_time)
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/83.0.4103.53 Safari/537.36'
        })
        return self._driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Closing browser")
        if hasattr(self, '_driver'):
            self._driver.quit()

class BerlinBot:
    def __init__(self):
        self.wait_time = 5
        self._sound_file = os.path.join(os.getcwd(), "alarm.wav")
        self._error_message = """There are currently no appointments available for the selected service! Please"""
        self.people_queue = [
            {"name": "Statnik, Illia", "index": 56},
            {"name": "Buiankova, Maiia", "index": 12},
            {"name": "Ahmadi, Ezatullah", "index": 2},
            {"name": "Arkadev, Sergei", "index": 3},
            {"name": "Astasov, Ilja", "index": 4},
            {"name": "Bakulin, Efim", "index": 6},
            {"name": "Bindernagel, Dennis Erich", "index": 9},
            {"name": "Bischoff, Mandy", "index": 10},
            {"name": "Gellert, Daniel", "index": 17},
            {"name": "Hryhorieva, Iryna", "index": 23},
            {"name": "Konitzko, Vanessa Nadine", "index": 29},
            {"name": "Kortzer, Miriam Jasmina", "index": 32},
            {"name": "Lukashchuk, Viacheslav", "index": 37},
            {"name": "Murtaj, Lennart", "index": 40},
            {"name": "Neagus, Natalia", "index": 41},
            {"name": "Popovicenco, Vladislav", "index": 47},
            {"name": "Rinas, Erika", "index": 50},
            {"name": "Turaeva, Nargis Niyozmahmadovna", "index": 60},
            {"name": "Zadyraka, Denys", "index": 66}
        ]
        self.place_indexes = [12, 10, 9] 

    @staticmethod
    def visit_start_page(driver: webdriver.Edge):
        login = "A194095"
        logging.info("Visiting start page")
        driver.get("https://dsp.dekra.de/login/xhtml/mainpage.jsf")
        login_input = driver.find_element(By.XPATH, '//*[@id="loginForm-username"]')
        login_input.send_keys(login)

    @staticmethod
    def enter_password(driver: webdriver.Edge):
        password = "Adventure704."
        logging.info("Entering password")
        password_input = driver.find_element(By.XPATH, '//*[@id="loginForm-password"]')
        password_input.send_keys(password)

    @staticmethod
    def confirm_login(driver: webdriver.Edge):
        logging.info("Confirming login")
        driver.find_element(By.XPATH, '//*[@id="loginForm-loginLink"]').click()

    @staticmethod
    def click_first_option(driver: webdriver.Edge):
        logging.info("Selecting first option")
        driver.find_element(By.XPATH, '//*[@id="j_idt74-0-j_idt81-3-j_idt82-j_idt84-0-img-"]').click()

    @staticmethod
    def select_second_option(driver: webdriver.Edge):
        logging.info("Selecting second option")
        driver.find_element(By.XPATH, '//*[@id="header"]/ul[2]/li[3]/a').click()

    @staticmethod
    def select_ort(driver: webdriver.Edge):
        logging.info("Selecting ort")
        driver.find_element(By.XPATH, '//*[@id="scheduling-panel-form:j_idt55"]').click()
        time.sleep(1)

    @staticmethod
    def select_place(driver: webdriver.Edge, place_index):
        logging.info(f"Selecting place {place_index}")
        driver.find_element(By.XPATH, f'//*[@id="scheduling-panel-form:j_idt55_{place_index}"]').click()
        time.sleep(1)

    @staticmethod
    def the_next_week(driver: webdriver.Edge):
        logging.info("Selecting next week")
        for _ in range(5):
            try:
                driver.find_element(By.XPATH, f'//*[@id="scheduling-calendar-form"]/div/div[3]').click()
                time.sleep(1)
            except Exception as e:
                logging.error(f"An error occurred while selecting next week: {e}")
                break 

    @staticmethod
    def select_termin(driver: webdriver.Edge):
        logging.info("Selecting termin")
        slots = driver.find_elements(By.CSS_SELECTOR, '.slot.available')
        return slots

    @staticmethod
    def choose_person(driver: webdriver.Edge, person_index):
        logging.info(f"Selecting person with index {person_index}")
        person_dropdown = driver.find_element(By.XPATH, '//*[@id="j_idt196:j_idt245"]')
        person_dropdown.click()
        driver.find_element(By.XPATH, f'//*[@id="j_idt196:j_idt245_{person_index}"]').click()

    @staticmethod
    def create_termin(driver: webdriver.Edge, place: str, person: str):
        logging.info("Creating termin")
        driver.find_element(By.XPATH, '//*[@id="j_idt196:j_idt275"]').click()
        logging.info("Termin created successfully")
        
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        
        logging.info(f"Termin created at {place} for {person}")

    def handle_termins(self, driver):
        # while self.people_queue:
            for place_index in self.place_indexes:
                self.select_ort(driver)
                self.select_place(driver, place_index)
                slots = self.select_termin(driver)

                while slots and self.people_queue:
                    slot = slots.pop(0)
                    slot.click()
                    person = self.people_queue.pop(0)
                    self.choose_person(driver, person['index'])
                    self.create_termin(driver, place=f"Place {place_index}", person=person['name'])
                    slots = self.select_termin(driver)
                    time.sleep(1)

                if not slots:  
                    logging.info(f"No more slots at place index {place_index}. Moving to next place.")

                if not self.people_queue:
                    logging.info("All people have been assigned to terms.")
                    break

            # if not self.people_queue:
            #     logging.info("All people have been assigned to terms.")
            #     break

    def success(self):
        logging.info("!!!SUCCESS - do not close the window!!!!")
        if current_platform == 'Windows':
            while True:
                winsound.PlaySound(self._sound_file, winsound.SND_FILENAME)
                time.sleep(5)
        else:
            logging.info("Sound notification is only supported on Windows.")

    def perform_login(self):
        with WebDriver() as driver:
            try:
                self.visit_start_page(driver)
                self.enter_password(driver)
                self.confirm_login(driver)
                self.click_first_option(driver)
                self.select_second_option(driver)
                self.the_next_week(driver)
                self.handle_termins(driver)
                self.success()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    bot = BerlinBot()
    bot.perform_login()
