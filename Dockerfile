#Python base image
FROM python:3.8.10

#to set the working directory in the container
WORKDIR /app

#to copy the current directory contents into the container
COPY . /app

#to install the dependencies (e.g., requirements.txt)
RUN pip install -r requirements.txt

#to define environment variables
ENV FLASK_APP=main.py

#to expose the port the app will run on
EXPOSE 5002

#command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
#CMD ["flask", "run", "--host=172.21.0.1", "--port=5002"]
