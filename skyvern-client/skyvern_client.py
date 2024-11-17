import json
from typing import Any, Union

import requests
from pydantic import ValidationError

from utils import TaskGenerationPayload
from skyvern_utils import PromptEngine
from litellm import completion
import os
from dotenv import load_dotenv


class SkyvernClient:
    def __init__(self, base_url, api_key=None):
        """
        Initialize the SkyvernAPI with base URL and API key.

        :param base_url: The base URL of the API.
        :param api_key: The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key or os.getenv("SKYVERN_API_KEY")
        self.base_endpoint = f"{base_url}/api/v1"
        self.headers = self._get_headers()

    def _get_headers(self):
        """
        Generate headers for the request, including API key and Content-Type.
        """
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def _validate_task_data(self, task_data: Union[TaskGenerationPayload, str, dict[str, Any]]):
        match task_data:
            case TaskGenerationPayload():
                return task_data
            case str():
                try:
                    parsed_data = json.loads(task_data)
                    return TaskGenerationPayload.model_validate(parsed_data)
                except (json.JSONDecodeError, ValidationError) as e:
                    raise ValueError(f"Failed to parse JSON string into TaskGenerationPayload: {e}")
            case dict():
                try:
                    return TaskGenerationPayload.model_validate(task_data)
                except ValidationError as e:
                    raise ValueError(f"Failed to validate dictionary as TaskGenerationPayload: {e}")
            case _:
                raise ValueError("Input must be a TaskGenerationPayload, a JSON string, or a dictionary")

    def create_task(self, task_data: Union[TaskGenerationPayload, str, dict[str, Any]]):
        """
        Create a task by sending a POST request to the /api/v1/tasks endpoint.

        :param task_data: A dictionary containing the task data.
        :return: Response object from the server.
        """
        validated_data = self._validate_task_data(task_data)
        endpoint = f"{self.base_endpoint}/tasks"

        serialized_data = validated_data.model_dump_json()

        print(serialized_data)

        # Send the POST request
        response = requests.post(endpoint, headers=self.headers, data=serialized_data)

        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()

    def list_tasks(self):
        """
        Retrieve a list of all tasks.
        :return: A list of tasks as dictionaries.
        """
        endpoint = f"{self.base_endpoint}/tasks"
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_task(self, task_id):
        """
        Retrieve details of a specific task by ID.
        :param task_id: The ID of the task.
        :return: Task details as a dictionary.
        """
        endpoint = f"{self.base_endpoint}/tasks/{task_id}"
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def update_task(self, task_id, updated_details):
        """
        Update a specific task's details.
        :param task_id: The ID of the task.
        :param updated_details: A dictionary with updated task details.
        :return: Updated task details as a dictionary.
        """
        endpoint = f"{self.base_endpoint}/tasks/{task_id}"
        response = requests.patch(endpoint, headers=self.headers, json=updated_details)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def delete_task(self, task_id):
        """
        Delete a specific task by ID.
        :param task_id: The ID of the task.
        :return: Response status or confirmation as a dictionary.
        """
        endpoint = f"{self.base_url}/tasks/{task_id}"
        response = requests.delete(endpoint, headers=self.headers)

        if response.status_code == 204:
            return response.json()
        else:
            response.raise_for_status()

    def generate_task_data(self):
        # TODO
        user_prompt = "go to target.com"

        prompt_engine = PromptEngine()

        prompt = prompt_engine.load_prompt("generate-task", user_prompt=user_prompt)

        # auth: run 'gcloud auth application-default'
        os.environ["VERTEX_PROJECT"] = "playground-0-ac4d"
        os.environ["VERTEX_LOCATION"] = "us-central1"

        response = completion(
            model="chat-bison",
            messages=[{"content": "Hello, how are you?", "role": "user"}]
        )

        print(response)


if __name__ == "__main__":
    # Initialize client; use https://api.skyvern.com/ for the cloud-hosted skyvern
    load_dotenv()
    client = SkyvernClient("http://localhost:8000")

    # Retrieve all tasks
    all_tasks = client.list_tasks()

    # Get an existing task by ID
    print(client.get_task(all_tasks[0]["task_id"]))

    # Create a new task
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
