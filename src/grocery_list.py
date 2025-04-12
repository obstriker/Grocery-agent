from pathlib import Path

from agno.agent import Agent
from agno.tools.file import FileTools
from agno.models.openai import OpenAIChat
from agno.agent import Agent, AgentMemory
from dotenv import load_dotenv
from agno.storage.agent.sqlite import SqliteAgentStorage
from os import getenv
from webtool import *

load_dotenv()

api_key = getenv("QDRANT_API_KEY")
qdrant_url = getenv("QDRANT_URL")

agent = Agent(tools=[FileTools(), get_info_from_website],
              model=OpenAIChat(id="gpt-4o-mini"),
              memory=AgentMemory(),
              storage=SqliteAgentStorage(table_name="agent_sessions", db_file="agent_storage.db"),
              add_history_to_messages=True,  # Adds recent chat history when generating a reply
              num_history_responses=3,       # Number of responses to include in context
              instructions=""""
You are a helpful grocery assistant. Your primary functions are:
1. Manage a grocery list stored in grocery_list.txt in hebrew
2. Add or remove individual items from the grocery list
3. Add ingredients from recipes to the grocery list
4. Organize items by category (produce, dairy, meat, etc.)
5. Check for duplicate items and consolidate quantities
6. Add items from URL recipes to the grocery list

When adding items:
- Maintain categorization of items
- Suggest alternatives when appropriate

When adding recipes:
- Extract all ingredients from the recipe
- Add ingredients to the appropriate categories
- Consider quantities needed for the recipe
- Ask for clarification

When removing items:
- Confirm removal of items
- Update quantities rather than removing if the user might want to keep some

Always maintain the grocery_list.txt file with current items, organized by category.

When starting a new conversation, read the current grocery_list.txt to understand what's already on the list.

When adding or removing items, make sure to update the grocery_list.txt file accordingly.
If the user says that he has some of the grocery at home then remove it from the list.

              """, show_tool_calls=True)