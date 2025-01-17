from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

class TestValidation:
    def test_get_agent_details(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
        driver.get('http://172.18.0.1:5000')
        a_items = driver.find_elements(by=By.TAG_NAME, value='a')
        assert len(a_items) == 2
        time.sleep(5)
        a_items[0].click()
        time.sleep(5)
        agent_item = driver.find_element(by=By.CLASS_NAME, value='agent')
        assert agent_item.text == 'wayne bob (pasla)'
        driver.quit()