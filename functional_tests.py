from selenium import webdriver
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
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "Actually finish the damn TDD tutorial" into a text box
        # (Manuels hobby is not finishing coding tutorials)

        # When he hits enter, the page updates, and now the page lists
        # "1: Finish the TDD tutorial" as an item in a to-do list

        # There is stll a text box inviting her to add another item. He
        # enters "Create a website that is not a to-do list" (Manuel loves
        # To-Do lists, but I think he can go a bit further)

        # The page updates again, and now it shows both items on his list

        # Manuel wonders wheter the site will remember her list. Then he
        # sees that the site has generated a unique URL for him -- there is
        # some explanotory text to that effect.

        # He visists that URL -- his to-do list is still there.

        # Satisfied he goes back to slepp.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
