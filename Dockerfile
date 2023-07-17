# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the bot.py and requirements.txt into the container
COPY bot.py .
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables
ENV TOKEN="6321386628:AAH6eXmLmb5qfl3CjUmQMlz9gL7jMJY8_No"
ENV AUTHORIZED_USERS="[6388590233]"

# Run the bot.py script using the environment variables
CMD ["python", "bot.py"]
