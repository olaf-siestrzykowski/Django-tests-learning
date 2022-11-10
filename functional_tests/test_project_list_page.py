from selenium import webdriver
from selenium.webdriver.common.by import By
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestProjectListPage(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_no_projects_alert(self):
        self.browser.get(self.live_server_url)

        alert = self.browser.find_element(By.CLASS_NAME, 'noproject-wrapper')
        self.assertEquals(
            alert.find_element(By.TAG_NAME, 'h3').text,
            'Sorry, you don\'t have any projects, yet.'
        )

    def test_no_projects_alert_button_redirects(self):
        self.browser.get(self.live_server_url)

        add_url = self.live_server_url + reverse('add')
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            add_url
        )

    def test_user_sees(self):
        project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

        self.browser.get(self.live_server_url)
        self.assertEquals(
            self.browser.find_element(By.TAG_NAME, 'h5').text,
            'project1'
        )

    def test_user_redirected_to_details(self):
        project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

        self.browser.get(self.live_server_url)
        detail_url = self.live_server_url + reverse('detail', args=[project1.slug])
        self.browser.find_element(By.LINK_TEXT, 'VISIT').click()
        self.assertEquals(
            self.browser.current_url,
            detail_url
        )
