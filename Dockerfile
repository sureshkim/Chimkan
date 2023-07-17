# Use the official Python image as the base image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create a working directory inside the container
WORKDIR /app

# Copy the bot.py file and requirements.txt to the container
COPY bot.py requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (if your bot needs a port to listen to incoming updates)
# EXPOSE 8443

# Set the environment variables (replace YOUR_TELEGRAM_BOT_TOKEN and YOUR_AUTHORIZED_USER_ID with actual values)
ENV TOKEN="6321386628:AAH6eXmLmb5qfl3CjUmQMlz9gL7jMJY8_No"
ENV AUTHORIZED_USERS="[6388590233]"

# Run the bot.py script (specify the worker process command here)
CMD ["python", "bot.py"]
