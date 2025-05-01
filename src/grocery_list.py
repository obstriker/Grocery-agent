import os
import json
from pathlib import Path
from dotenv import load_dotenv

from agno.agent import Agent, AgentMemory
from agno.tools.file import FileTools
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from webtool import get_info_from_website

# Load environment variables
load_dotenv()

# File path and environment setup
grocery_path = 'grocery_list.txt'

# Create the grocery file if it doesn't exist
if not os.path.exists(grocery_path):
    with open(grocery_path, 'w', encoding='utf-8') as f:
        f.write('')

def save_grocery_list(content: str) -> str:
    """Overwrite the grocery list with new content."""
    try:
        dir_name = os.path.dirname(grocery_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(grocery_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"status": "success"})
    except OSError as e:
        print(f"ERROR    Error saving to file: {e}")
        return json.dumps({"status": "failed", "error": str(e)})

def read_grocery_list() -> str:
    """Read the current grocery list."""
    try:
        with open(grocery_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return json.dumps({"content": content})
    except FileNotFoundError:
        return json.dumps({"status": "failed", "error": "File does not exist"})

agent = Agent(tools=[save_grocery_list, read_grocery_list, get_info_from_website],
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

When not returning a grocery list keep your answers short upto one sentence
              """, show_tool_calls=True)