import time
import os
import logging
import threading
from platform import system as platform_system
from selenium import webdriver
from selenium.webdriver.common.by import By
import winsound

current_platform = platform_system()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Edge
        self._implicit_wait_time = 3

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

    def __exit__(self):
        logging.info("Closing browser")
        if hasattr(self, '_driver'):
            self._driver.quit()

class BerlinBot:
    def __init__(self):
        self.wait_time = 3
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
        ]
        self.bike_people_queue = [
            {"name": "Artamonov, Aleksei", "index": 2},
            {"name": "Stikus, Valerijs", "index": 7},
        ]
        self.place_indexes = [15, 10, 9, 12]

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
    def select_class(driver: webdriver.Edge):
        logging.info("Selecting class")
        driver.find_element(By.XPATH, '//*[@id="scheduling-panel-form:j_idt62"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="scheduling-panel-form:j_idt62_3"]').click()

    @staticmethod
    def select_b_class(driver: webdriver.Edge):
        logging.info("Selecting class")
        driver.find_element(By.XPATH, '//*[@id="scheduling-panel-form:j_idt62"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="scheduling-panel-form:j_idt62_4"]').click()

    @staticmethod
    def reset_to_current_week(driver: webdriver.Edge):
        logging.info("Resetting to approximately four weeks back")
        try:
            for _ in range(5):
                prev_button = driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[1]')
                prev_button.click()
                time.sleep(2)
            logging.info("Returned approximately four weeks back.")
        except Exception as e:
            logging.error(f"An error occurred while resetting to four weeks back: {e}")

    @staticmethod
    def play_sound_for_duration(sound_file: str, duration: int):
        """Play sound for a specific duration in seconds."""
        def play_sound():
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
        time.sleep(duration)
        
        winsound.PlaySound(None, winsound.SND_PURGE)

    @staticmethod
    def create_termin(driver: webdriver.Edge, place: str, person: str):
        logging.info("Creating termin")
        driver.find_element(By.XPATH, '//*[@id="j_idt196:j_idt275"]').click()
        logging.info("Termin created successfully")

        BerlinBot.play_sound_for_duration(self._sound_file, 2)
        
        logging.info(f"Termin created at {place} for {person}")

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

    def the_next_week(self, driver: webdriver.Edge, max_weeks=5):
        logging.info("Selecting next week")
        for i in range(max_weeks):
            logging.info(f"Checking week {i+1}")
            try:
                slots = BerlinBot.select_termin(driver)
                if slots:
                    logging.info("Available slots found.")
                    return slots
                driver.find_element(By.XPATH, f'//*[@id="scheduling-calendar-form"]/div/div[3]').click()
                time.sleep(2)
            except Exception as e:
                logging.error(f"An error occurred while selecting next week: {e}")
                break
        logging.info("No available slots found in the next weeks.")
        return []

    def handle_termins(self, driver):
        while self.people_queue or self.bike_people_queue:
            for place_index in self.place_indexes:
                self.select_ort(driver)
                self.select_place(driver, place_index)

                if place_index == 15:
                    self.select_class(driver)
                    logging.info("Handling motorcycles. Clicking next week 4 times.")
                    
                    for _ in range(4):
                        driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[3]').click()
                        time.sleep(1)

                    slots = BerlinBot.select_termin(driver)
                    while slots and self.bike_people_queue:
                        slot = slots.pop(0)
                        try:
                            slot.click()
                            person = self.bike_people_queue.pop(0)
                            BerlinBot.choose_person(driver, person['index'])
                            BerlinBot.create_termin(driver, place=f"Place {place_index}", person=person['name'])
                            slots = BerlinBot.select_termin(driver)
                            time.sleep(1)
                        except Exception as e:
                            logging.error(f"Failed to click the slot or create termin: {e}")
                            continue 
                    
                    logging.info("Resetting to the current week after handling motorcycles.")
                    self.reset_to_current_week(driver)

                    continue

                else:
                    for _ in range(5):
                        self.select_b_class(driver)
                        slots = self.the_next_week(driver)
                        if not slots:
                            logging.info("No more slots available, moving to the next place.")
                            break

                        while slots and self.people_queue:
                            slot = slots.pop(0)
                            try:
                                slot.click()
                                person = self.people_queue.pop(0)
                                BerlinBot.choose_person(driver, person['index'])
                                BerlinBot.create_termin(driver, place=f"Place {place_index}", person=person['name'])
                                slots = BerlinBot.select_termin(driver)
                                time.sleep(1)
                            except Exception as e:
                                logging.error(f"Failed to click the slot or create termin: {e}")
                                continue

                    logging.info("Resetting to the current week after handling regular appointments.")
                    self.reset_to_current_week(driver)

                logging.info(f"Moving to the next place after processing current place.")
                continue

            if not self.people_queue and not self.bike_people_queue:
                logging.info("All people have been assigned to terms.")
                break

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
                self.handle_termins(driver)
                self.success()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    bot = BerlinBot()
    bot.perform_login()
