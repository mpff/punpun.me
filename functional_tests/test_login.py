import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager

from .base import FunctionalTest

SUBJECT = 'Your login link for punpun.me'


class LoginTest(FunctionalTest):

    @contextmanager
    def pop_inbox(self):
        try:
            inbox = poplib.POP3_SSL('imap.migadu.com', 995)
            inbox.user(os.environ['MIGADU_USER'])
            inbox.pass_(os.environ['MIGADU_PASSWORD'])
            yield inbox

        finally:
            inbox.quit()


    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        start = time.time()
        while time.time() - start < 60:
            with self.pop_inbox() as inbox:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        inbox.dele(i)
                        body = '\n'.join(lines)
                        return body
            time.sleep(5)


    def test_can_get_email_link_to_log_ing(self):
        # Edith goes to the awesome lists site and notices
        # a "Log in" section in the navbar for the first time

        # It's telling her to enter her emai address, so she does
        if self.staging_server:
            test_email = 'testing@punpun.me'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)

        self.browser.find_element_by_name('email').send_keys(test_email)

        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an emai has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
            ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has an url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

