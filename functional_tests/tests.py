from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 4


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Manuel wants to try his cool online to-do app. He goes to check out
        # its homepage.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Actually finish the damn TDD tutorial" into a text box
        # (Manuels hobby is not finishing coding tutorials)
        inputbox.send_keys('Actually finish the damn TDD tutorial')

        # When he hits enter, the page updates, and now the page lists
        # "1: Actually finish the damn TDD tutorial" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Actually finish the damn TDD tutorial')

        # There is stll a text box inviting her to add another item. He
        # enters "Create a website that is not a to-do list" (Manuel loves
        # To-Do lists, but I think he can go a bit further)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Create a website that is not a to-do list')
        inputbox.send_keys(Keys.ENTER)
        

        # The page updates again, and now it shows both items on his list
        self.wait_for_row_in_list_table('2: Create a website that is not a to-do list')
        self.wait_for_row_in_list_table('1: Actually finish the damn TDD tutorial')

        # Satisfied he goes back to sleep.



    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Manuel starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Actually finish the damn TDD tutorial')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Actually finish the damn TDD tutorial')

        # He notices that his list has an unique URL
        manuel_list_url = self.browser.current_url
        self.assertRegex(manuel_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Manuel's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Actually finish the damn TDD tutorial', page_text)
        self.assertNotIn('Create a website that is not a to-do list', page_text)

        # Francis starts a new list by entering a new item. He is less 
        # interesting than Manuel's...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, manuel_list_url)

        # Again, there is no trace of Manuel's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Actually finish the damn TDD tutorial', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
