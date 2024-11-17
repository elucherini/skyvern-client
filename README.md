# skyvern-client
A lightweight Python-based Skyvern client

## Usage
- Create a `.env` file in the root with your Skyvern API key. An example is provided in `.env_example`.
- Use this library!

```python
from dotenv import load_dotenv
from skyvern_client import SkyvernClient

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
```

## FAQ

#### 1. Do I need an LLM to use this library?

No, but the Skyvern UI uses an LLM to generate the payload for task generation. That functionality will be 
available soon. For now, I have imported the prompt used by Skyvern in `skyvern-prompts/generate-task.j2`. Feel free to
prompt your LLM of choice with that prompt and lightly parse the output before calling `create_task`.