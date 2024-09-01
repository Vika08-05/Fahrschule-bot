import time
import os
import logging
import threading
from platform import system as platform_system
from selenium import webdriver
from selenium.webdriver.common.by import By
import winsound

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver = None
        self._implicit_wait_time = 3

    def __enter__(self):
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

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info("Closing browser")
        if self._driver:
            self._driver.quit()

class BerlinBot:
    def __init__(self):
        self.wait_time = 3
        self._sound_file = os.path.join(os.getcwd(), "alarm.wav")
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

    def visit_start_page(self, driver):
        login = "A194095"
        logging.info("Visiting start page")
        driver.get("https://dsp.dekra.de/login/xhtml/mainpage.jsf")
        driver.find_element(By.XPATH, '//*[@id="loginForm-username"]').send_keys(login)

    def enter_password(self, driver):
        password = "Adventure704."
        logging.info("Entering password")
        driver.find_element(By.XPATH, '//*[@id="loginForm-password"]').send_keys(password)

    def confirm_login(self, driver):
        logging.info("Confirming login")
        driver.find_element(By.XPATH, '//*[@id="loginForm-loginLink"]').click()

    def select_option(self, driver, option_xpath):
        logging.info(f"Selecting option {option_xpath}")
        driver.find_element(By.XPATH, option_xpath).click()
        time.sleep(1)


    def reset_to_current_week(self, driver):
        logging.info("Resetting to approximately four weeks back")
        for _ in range(5):
            try:
                driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[1]').click()
                time.sleep(1)
            except Exception as e:
                logging.error(f"An error occurred while resetting to four weeks back: {e}")
                break
        logging.info("Returned approximately four weeks back.")

    def play_sound_for_duration(self, duration):
        """Play sound for a specific duration in seconds."""
        def play_sound():
            winsound.PlaySound(self._sound_file, winsound.SND_FILENAME)
        
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
        time.sleep(duration)
        winsound.PlaySound(None, winsound.SND_PURGE)

    def create_termin(self, driver, place, person):
        logging.info("Creating termin")
        driver.find_element(By.XPATH, '//*[@id="j_idt196:j_idt275"]').click()
        self.play_sound_for_duration(2)
        logging.info(f"Termin created at {place} for {person}")

    def select_termin(self, driver):
        logging.info("Selecting termin")
        return driver.find_elements(By.CSS_SELECTOR, '.slot.available')
    

    def choose_person(self, driver, person_index):
        logging.info(f"Selecting person with index {person_index}")
        driver.find_element(By.XPATH, '//*[@id="j_idt196:j_idt245"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, f'//*[@id="j_idt196:j_idt245_{person_index}"]').click()

    def the_next_week(self, driver, max_weeks=5):
        logging.info("Selecting next week")
        for i in range(max_weeks):
            slots = self.select_termin(driver)
            if slots:
                logging.info("Available slots found.")
                return slots
            try:
                driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[3]').click()
                time.sleep(2)
            except Exception as e:
                logging.error(f"An error occurred while selecting next week: {e}")
                break
        logging.info("No available slots found in the next weeks.")
        return []

    def handle_termins(self, driver):
        cycle_count = 0
        b_class_selected = False  

        while self.people_queue or self.bike_people_queue:
            for place_index in self.place_indexes:
                self.select_option(driver, '//*[@id="scheduling-panel-form:j_idt55"]')
                time.sleep(1)
                self.select_option(driver, f'//*[@id="scheduling-panel-form:j_idt55_{place_index}"]')
                time.sleep(1)

                if place_index == 15:
                    self.select_option(driver, '//*[@id="scheduling-panel-form:j_idt62"]')
                    time.sleep(1)
                    self.select_option(driver, '//*[@id="scheduling-panel-form:j_idt62_3"]')
                    time.sleep(1)
                    
                    logging.info("Handling motorcycles. Clicking next week 5 times.")
                    for _ in range(5):
                        driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form"]/div/div[3]').click()
                        time.sleep(1)

                    slots = self.select_termin(driver)
                    while slots and self.bike_people_queue:
                        slot = slots.pop(0)
                        try:
                            slot.click()
                            person = self.bike_people_queue.pop(0)
                            
                            if self.is_error_present(driver):
                                logging.warning("Error detected, skipping to the next participant.")
                                continue

                            self.choose_person(driver, person['index'])
                            self.create_termin(driver, f"Place {place_index}", person['name'])
                            slots = self.select_termin(driver)
                        except Exception as e:
                            logging.error(f"Failed to click the slot or create termin: {e}")

                    self.reset_to_current_week(driver)

                else:
                    if not b_class_selected:
                        self.select_option(driver, '//*[@id="scheduling-panel-form:j_idt62"]')
                        time.sleep(1)
                        self.select_option(driver, '//*[@id="scheduling-panel-form:j_idt62_4"]')
                        b_class_selected = True  

                    for _ in range(5):
                        slots = self.the_next_week(driver)
                        if not slots:
                            break
                        while slots and self.people_queue:
                            slot = slots.pop(0)
                            try:
                                slot.click()
                                person = self.people_queue.pop(0)
                                
                                if self.is_error_present(driver):
                                    logging.warning("Error detected, skipping to the next participant.")
                                    continue

                                self.choose_person(driver, person['index'])
                                self.create_termin(driver, f"Place {place_index}", person['name'])
                                slots = self.select_termin(driver)
                            except Exception as e:
                                logging.error(f"Failed to click the slot or create termin: {e}")

                    self.reset_to_current_week(driver)

                cycle_count += 1

                if cycle_count % 2 == 0:
                    logging.info("Moving back a week after every 2rd cycle.")
                    while True:
                        back_button = driver.find_element(By.XPATH, '//*[@id="scheduling-calendar-form:j_idt75"]')
                        if 'ui-state-disabled' in back_button.get_attribute('class'):
                            logging.info("The back button is disabled, returning to the earliest possible week.") 
                            break 
                        back_button.click()     
                        time.sleep(1)
                    
                logging.info("Returned to the earliest week. Continuing to search for appointments.")

                logging.info(f"Moving to the next place after processing current place.")
                continue

            if not self.people_queue and not self.bike_people_queue:
                logging.info("All people have been assigned to terms.")
                break

    def is_error_present(self, driver):
        """Перевіряє наявність елемента з помилкою."""
        try:
            error_element = driver.find_element(By.XPATH, '//*[@id="j_idt196:dialogAppointmentS00001000000001742726055CBFNEUT13H20_content"]/ul[1]')
            if error_element.is_displayed():
                return True
        except:
            pass
        return False


    def success(self):
        logging.info("!!!SUCCESS - do not close the window!!!!")
        if platform_system() == 'Windows':
            while True:
                winsound.PlaySound(self._sound_file, winsound.SND_FILENAME)
                time.sleep(3)
        else:
            logging.info("Sound notification is only supported on Windows.")

    def perform_login(self):
        with WebDriver() as driver:
            try:
                self.visit_start_page(driver)
                self.enter_password(driver)
                self.confirm_login(driver)
                self.select_option(driver, '//*[@id="j_idt74-0-j_idt81-3-j_idt82-j_idt84-0-img-"]')
                self.select_option(driver, '//*[@id="header"]/ul[2]/li[3]/a')
                self.handle_termins(driver)
                self.success()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    bot = BerlinBot()
    bot.perform_login()
