from selenium import webdriver
from time import sleep, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pdb
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class JWCBooker:
    def __init__(self, court_number=1, show_window=False, poll_time_seconds=120, poll_interval_seconds=0.005):
        options = Options()
        if not show_window:
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            "/Users/jg/Downloads/bookingBots/chromedriver",
            options=options
        )
        self.booking_site_url = 'https://secure.recreation.ucla.edu/booking'

        self.court_number = court_number
        self.poll_time_seconds = poll_time_seconds
        self.poll_interval_seconds = poll_interval_seconds

        self.init_connection()

    def init_connection(self):
        self.driver.get(self.booking_site_url)

        sign_in_link = self.driver.find_element(By.LINK_TEXT, "Sign In")
        sign_in_link.click()

        self.driver.implicitly_wait(1)
        signOn_button = self.driver.find_element(By.XPATH, "//*[@id='section-sign-in-first']/div[6]/div/button")
        sleep(1)
        # self.driver.implicitly_wait(10)
        signOn_button.click()
        # ActionChains(self.driver).move_to_element(signOn_button).click(signOn_button).perform()

        self.driver.find_element(By.ID, 'logon').send_keys('user')
        self.driver.find_element(By.ID, 'pass').send_keys('password')

        ucla_signIn = self.driver.find_element(By.XPATH, "//*[@id='sso']/form/div/table/tbody/tr/td[1]/button")
        ucla_signIn.click()

        WebDriverWait(self.driver, 20)\
            .until(EC.element_to_be_clickable((By.LINK_TEXT, "JWC - Badminton Ct #%d" % self.court_number)))\
            .click()

        self.ready_to_poll_time = time()

    def make_reservation(self):
        # pdb.set_trace()
        try:
            t1 = time()
            # self.driver.refresh()
            # print(time() - t1)
            select_date_button = self.driver.find_element(By.XPATH, "//*[@id='mainContent']/div[2]/div[9]/div[3]/div[1]/button")
            self.driver.execute_script("arguments[0].click();", select_date_button)
            print(time() - t1)
            # WebDriverWait(self.driver, 5) \
            #     .until(EC.element_to_be_clickable((By.XPATH, "//*[@id='modalSingleDateSelector']/div/div/div[2]/div/div/button[2]"))) \
            #     .click()
            # print(time() - t1)
            next_date_button = self.driver.find_element(By.XPATH, "//*[@id='modalSingleDateSelector']/div/div/div[2]/div/div/button[2]")
            next_date_button.click()
            print(time() - t1)
            apply_date_button = self.driver.find_element(By.XPATH, "//*[@id='modalSingleDateSelector']/div/div/div[2]/button")
            apply_date_button.click()
            print(time()-t1)

            # self.driver.refresh()
            # print(time() - t1)
        except Exception as e:
            print(e)

        return False

    def try_booking(self):
        try_num = 0

        while True:
            # try to get ticket
            reservation_completed = self.make_reservation()

            if reservation_completed:
                print('Got a ticket!!')
                break
            elif time() - self.ready_to_poll_time > self.poll_time_seconds:
                print(f'Tried {try_num} times, but couldn\'t get tickets..')
                break
            else:
                self.driver.refresh()
                sleep(self.poll_interval_seconds)
                try_num += 1


booker = JWCBooker(show_window=True)
booker.make_reservation()

# booker.driver.close()