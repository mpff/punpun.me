from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Manuel goes to the home page and accidentally tries to submit
        # an empty list item. He hits Enter on the empty input box

        # The home page refershes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item, which works

        # Perversely, he now decides to submit a second blank list item

        # He recieves a similir warning on the list page

        # And he can correct it by filling some text in
        self.fail('write the test!')
