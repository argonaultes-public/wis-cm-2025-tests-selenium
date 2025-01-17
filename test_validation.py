from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import pytest

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.models import Base, Agent


load_dotenv()

@pytest.fixture
def agents():
    engine = create_engine(os.getenv('DB_URL'))
    session = Session(engine)
    Base.metadata.create_all(engine)
    waynebob = Agent(photo='pasla', prenom='bob', nom='wayne')
    clarkkent = Agent(photo='/path/to/photo', prenom='clark', nom='kent')
    session.add_all([waynebob, clarkkent])
    session.commit()
    return list(map(str, [waynebob, clarkkent]))

class TestValidation:

    def setup_method(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
#        options.add_argument("--headless")
#        driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
        self.driver = webdriver.Firefox(options=options)


    def test_get_agent_details(self, agents):
        self.driver.get('http://localhost:5000')
        a_items = self.driver.find_elements(by=By.TAG_NAME, value='a')
        assert len(a_items) == len(agents)
        time.sleep(5)
        a_items[0].click()
        time.sleep(5)
        agent_item = self.driver.find_element(by=By.CLASS_NAME, value='agent')
        assert agent_item.text == agents[0]

    def teardown_method(self):
        self.driver.quit()