# Use the official Python image as a base image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app
#COPY ./dolarBrecha.sql /docker-entrypoint-initdb.d/


# Install dependencies
RUN pip install --upgrade pip
# Install dependencies
RUN pip install --upgrade pip \
    && pip install requests \
    && pip install beautifulsoup4 \
    && pip install python-telegram-bot \
    && pip install mysql-connector-python

# Run the application
CMD ["python", "main.py"]

