import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app.models import User
from app import create_app, db as _db

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

class TestHabitTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(10)  # Implicit wait for elements to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_title(self):
        self.driver.get("http://localhost:5000")  # Replace with your app's URL
        self.assertIn("Habit Tracker", self.driver.title)

    def test_login_page(self):
        self.driver.get("http://localhost:5000/login")  # Replace with your app's login URL
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.NAME, "submit")

        username_field.send_keys("test")
        password_field.send_keys("test123")
        login_button.click()

        # Wait for the next page to load and check for a specific element
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        self.assertIn("Dashboard", self.driver.page_source)

    def test_dashboard_page(self):
        self.driver.get("http://localhost:5000/dashboard")
        # Check for specific elements on the dashboard page
        self.assertIn("Your Habits", self.driver.page_source)
        self.assertIn("Add Habit", self.driver.page_source)
        self.assertIn("Habit List", self.driver.page_source)
        # Add more assertions as needed
    
    def test_weekly_summary_page(self):
        self.driver.get("http://localhost:5000/weekly")
        # Check for specific elements on the weekly summary page
        self.assertIn("Weekly Summary", self.driver.page_source)
        self.assertIn("Habit Progress", self.driver.page_source)
        # Add more assertions as needed

    def test_monthly_page(self):
        self.driver.get("http://localhost:5000/monthly")
        # Check for specific elements on the monthly page
        self.assertIn("Monthly Summary", self.driver.page_source)
        self.assertIn("Habit Progress", self.driver.page_source)
        # Add more assertions as needed

    def test_yearly_page(self):
        self.driver.get("http://localhost:5000/yearly")
        # Check for specific elements on the yearly page
        self.assertIn("Yearly Summary", self.driver.page_source)
        self.assertIn("Habit Progress", self.driver.page_source)
        # Add more assertions as needed

