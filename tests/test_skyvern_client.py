import pytest
from skyvern_client import SkyvernClient
import requests
import os
from dotenv import load_dotenv


class TestSkyvernClient:
    @pytest.fixture
    def client(self):
        load_dotenv()
        return SkyvernClient("http://localhost:8000", os.getenv("SKYVERN_API_KEY"))

    def test_list_tasks(self, client):
        try:
            client.list_tasks()
        except requests.HTTPError as e:
            pytest.fail(f"list_tasks raised an HTTPError!\n{e}")

    def test_get_task(self, client):
        all_tasks = client.list_tasks()

        try:
            client.get_task(all_tasks[0]["task_id"])
        except requests.HTTPError as e:
            pytest.fail(f"get_task raised an HTTPError!\n{e}")

    def test_create_task(self, client):
        task_payload = {
            "title": "my title",
            "url": "https://www.target.com",
            "webhook_callback_url": None,
            "navigation_goal": "Go to target.com and add any item to the cart. COMPLETE when an item has been added to "
                               "the cart and the cart is not empty. Do not add more than one item to the cart.",
            "data_extraction_goal": None,
            "proxy_location": "RESIDENTIAL",
            "navigation_payload": None,
            "extracted_information_schema": None,
            "totp_verification_url": None,
            "totp_identifier": None,
            "error_code_mapping": None
        }

        client.create_task(task_payload)

        # Check that the newly created task is in the tasks
        all_tasks = client.list_tasks()
        for task in all_tasks:
            if task["request"]["title"] == task_payload["title"]:
                return
        pytest.fail("Failed to find newly created task in the list of all tasks -- task might not have been created")
