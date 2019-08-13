from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Manuel wants to try his cool online to-do app. He goes to check out
        # its homepage.
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)


        # There is stll a text box inviting her to add another item. He
        # enters "Create a website that is not a to-do list" (Manuel loves
        # To-Do lists, but I think he can go a bit further)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Create a website that is not a to-do list')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        

        # The page updates again, and now it shows both items on his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '1: Actually finish the damn TDD tutorial', 
            [row.text for row in rows]
            )
        self.assertIn(
            '2: Create a website that is not a to-do list', 
            [row.text for row in rows]
            )

        # Manuel wonders wheter the site will remember her list. Then he
        # sees that the site has generated a unique URL for him -- there is
        # some explanotory text to that effect.
        self.fail('Finish the test!')

        # He visists that URL -- his to-do list is still there.

        # Satisfied he goes back to slepp.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
