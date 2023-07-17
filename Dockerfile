# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the bot.py file and requirements.txt into the container
COPY bot.py .
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables (replace with your actual values)
ENV TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
ENV AUTHORIZED_USERS="[123456789, 987654321]"

# Run the bot.py script
CMD ["python", "bot.py"]
