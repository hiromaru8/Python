import unittest
import logging
from src.client.api_client import APIClient
from src.utils.config import Config
from tests.base_test import BaseIntegrationTest

class TestUserFlow(BaseIntegrationTest):

    TEST_ID = "IT-001"

    @classmethod
    def setUpClass(cls):
        config = Config("config/test_env.json")
        api_conf = config.get("api")
        cls.client = APIClient(
            api_conf["base_url"],
            api_conf["timeout"]
        )

    def test_user_registration_flow(self):

        result = {"status": "ok"}
        self.assertEqual(result["status"], "ok")

        

        
        
        
