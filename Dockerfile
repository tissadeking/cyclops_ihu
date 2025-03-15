# Use a Python base image
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the dependencies (e.g., requirements.txt)
RUN pip install -r requirements.txt

# Define environment variables
ENV FLASK_APP=main.py

# Expose the port the app will run on
EXPOSE 5002

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
#CMD ["flask", "run", "--host=172.21.0.1", "--port=5002"]
