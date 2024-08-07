"""Example of using PandasAI with am Excel file."""

import os

from datahorse import Agent

# Betas & Bludgers Writing Competitions List (source: https://heystacks.com/?type=sheets&tags=data)
google_sheets_url = "https://docs.google.com/spreadsheets/d/1VKkhugv2eF87AoOm4OXjI0sQEHrNhxy6gPL3F7xyw7g/edit#gid=115719017"  # noqa E501

# By default, unless you choose a different LLM, it will use BambooLLM.
# You can get your free API key signing up at https://datahorse.ai/ (you can also configure it in your .env file)
os.environ["DATAHORSE_API_KEY"] = "your-api-key"

agent = Agent(google_sheets_url)
response = agent.chat("How many short stories are there?")
print(response)
# Output: 35
