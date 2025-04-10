import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestExitIntent(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(5)
        self.url = "https://the-internet.herokuapp.com/exit_intent"

    def test_exit_intent_modal(self):
        driver = self.driver
        driver.get(self.url)
        self.assertIn("The Internet", driver.title)

        driver.maximize_window()
        time.sleep(2)

        # Simulate exit intent
        self.trigger_exit_intent(driver)

        # Increase wait time for modal to appear
        try:
            print("Waiting for modal to appear...")
            modal = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "ouibounce-modal")),
                message="Exit intent modal did not become visible"
            )
            print("Modal appeared, verifying its contents...")

            self.assertTrue(modal.is_displayed(), "Modal should be visible")

            title = modal.find_element(By.TAG_NAME, "h3").text.strip()
            self.assertEqual(title, "This is a modal window", "Unexpected modal title")

            print("✅ Modal appeared and is verified.")
        except Exception as e:
            print(f"❌ Error: {e}")
            driver.save_screenshot("modal_error.png")
            self.fail(f"❌ Modal did not appear: {e}")

    def trigger_exit_intent(self, driver):
        # Locate the body element
        body = driver.find_element(By.TAG_NAME, "body")

        # Simulate mouse movement to the top of the screen by moving to an element near the top
        actions = ActionChains(driver)
        actions.move_to_element(body).move_by_offset(0, -50).perform()  # Move 50 pixels upward
        time.sleep(2)  # Increased time to ensure exit intent has a chance to be triggered

        # Fallback: dispatch mouseout event to trigger the modal
        driver.execute_script("""
            const evt = new MouseEvent('mouseout', {
                clientY: 0,
                relatedTarget: null
            });
            document.dispatchEvent(evt);
        """)
        time.sleep(3)  # Increased time to wait for the modal after triggering the exit intent

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
