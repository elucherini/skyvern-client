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

#### 2. Where can I find my Skyvern API key?

Go to the Skyvern UI and click on Settings. Locate the "API Keys" section and click on Reveal.

Alternatively, you may want to create a task through a customized prompt with the UI. After submitting and next to the 
"Run" button, you will find a "cURL" button. This will copy the cURL request to your clipboard and will look like this:

```
curl 'https://api.skyvern.com/api/v1/tasks' -X POST -H "Content-Type: application/json" -H "x-api-key: abcde321.abcde1234.edabc321" --data-binary '{"title":null,"url":"https://www.target.com","webhook_callback_url":null,"navigation_goal":null,"data_extraction_goal":null,"proxy_location":"RESIDENTIAL","navigation_payload":"null","extracted_information_schema":null,"totp_verification_url":null,"totp_identifier":null,"error_code_mapping":null}'
```

Use a text editor to extract the value of `x-api-key`.

#### 3. Does this library work with Cloud or self-hosted Skyvern?

Both!