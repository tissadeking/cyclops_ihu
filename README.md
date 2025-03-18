# Intent-Based Human Interface (CyclOps)

This repository contains some not all of the components in the CyclOps Intent-based Human Interface (IHU).


## Installation

- Download the application code:
    ```
    git clone https://github.com/tissadeking/cyclops_ihu.git
    ```
- Change the current directory to cyclops_ihu.
    ```
    cd cyclops_ihu

- Build and run the software as Docker container:
    ```
    sudo docker-compose build
    sudo docker-compose up
    ```
## Accessing the service
- The API is available at http:127.0.0.1:5002 or any other IP with the same port.
- It shows the first page which a user clicks to enter the page through which they can register or login.
- For successful login, the NLP Chat or dc_net.py needs to be running. 

## Testing with NLP Chat
- To test with NLP Chat, go to the file main.py.
- Go to line 114 and change the URL from f"http://{host}:{dc_port}?userid={userid}" to the NLP Chat URL with userid as the path.
- Then follow the idea in dc_net.py to implement a method to allow successful loading of the NLP Chat through the URL with the userid.
- Then, build and run the Docker container as shown above.

## Testing with dc_net.py
- dc_net.py is only a replica of the verification system of the NLP Chat before a user is redirected to the chat.
- Build and run the software as it is on a terminal.
- Open another terminal instance, cd into the root folder of the project and run:
   ```
    python3 dc_net.py
- Then, go to the API above http:127.0.0.1:5002 on a browser and register and log in.
- A successful login redirects you to a page saying: "Welcome to NLP Chat! Your userid (xxxxxxxxxxxxxxxxxxxx) is valid."

## Testing with Info Retrieval
- The file put_response.py contains examples of exploratory and analytical intents with the API to send the intent: "http://127.0.0.1:5002/intent".
- This API is where the Info Retrieval is expected to send its structured intents.
- Build and run the software as it is on a terminal.
- Open a new terminal instance, cd into the root folder of the project and run:
   ```
    python3 put_response.py
- You can comment one example of an intent so as to test the interaction with the other example of an intent.

## Shutdown the service
- First stop the containers on the terminal and then run:
   ```
    sudo docker-compose down