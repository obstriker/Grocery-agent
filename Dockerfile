# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy project files (Python scripts, .env, grocery_list.txt)
COPY . .

# Install system packages required for building Python libraries and web scraping
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev

# Alternative manual install if requirements.txt is not provided
RUN pip install python-telegram-bot python-dotenv agno beautifulsoup4 chardet openai sqlalchemy

# Ensure SQLite database and text files are writable inside the container
RUN touch grocery_list.txt

# Set default environment variables (override at runtime if needed)
ENV TELEGRAM_KEY=<your_telegram_key_here>

# Expose a port for the bot (if applicable, optional)
EXPOSE 8080

# Set the default command to run the main Telegram bot script
CMD ["python", "src/bot.py"]
