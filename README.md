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
## Accessing the software
- The API is available at http:127.0.0.1:5002 or any other IP with the same port.
- It shows the first page which a user clicks to enter the page through which they can register or login.
- For successful login, the NLP Chat or dc_net.py needs to be running. 

## Testing with NLP Chat
- To test with NLP Chat, build and run the software as it is on a terminal.
- Line 127 of the main.py file contains the NLP Chat URL with userid as the path.
- Successful login redirects the user to NLP Chat with their userid.

## Testing with dc_net.py
- dc_net.py is only a replica of the verification system supposed to be provisioned by the NLP Chat before a user is redirected to the chat.
- Go to line 127 of the main.py file and change the NLP Chat URL to f"http://{host}:{dc_port}?userid={userid}".
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