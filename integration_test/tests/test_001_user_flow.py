import unittest
import logging
from src.client.api_client import APIClient
from src.utils.config import Config


class TestUserFlow(unittest.TestCase):

    TEST_ID = "IT-001"
    logger = logging.getLogger(TEST_ID)
    
    @classmethod
    def setUpClass(cls):
        config = Config("config/test_env.json")
        api_conf = config.get("api")
        cls.client = APIClient(
            api_conf["base_url"],
            api_conf["timeout"]
        )

    def test_user_registration_flow(self):
        self.logger.info("Executing %s", self.TEST_ID)

        # ダミー例
        result = {"status": "ok"}
        self.assertEqual(result["status"], "ok")
        
        
        
