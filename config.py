import yaml

#to retrieve configuration data from the config.yml file

#all files in the docker container are stored inside the folder app
files_directory = '/app/'
#reads and opens the yml file
yml_file = 'config.yml'
with open(yml_file) as f:
    parameters = yaml.safe_load(f)
    #print("yml accessed and opened")

#to retrieve ML tasks and models data from the tasks_models.yml file
tasks_models_file = 'tasks_models.yml'
with open(tasks_models_file) as f:
    task_parameters = yaml.safe_load(f)
    #print("tasks yml accessed and opened")

#groq api key for the llm-based functionalities
groq_api_key = parameters['groq_api_key']
#ihu host and port to deploy the container
host = parameters['host']
port = parameters['port']
#port for the script dc_net.py which replicates the connection to NLP Chat
dc_port = parameters['dc_port']

#files and folder used within the container
policy_store_directory = files_directory + parameters['policy_store_file']
current_user_directory = files_directory + parameters['current_user_file']
processed_data_directory = files_directory + parameters['processed_data_file']
retrieved_data_directory = files_directory + parameters['retrieved_data_file']
retrieved_data_folder = files_directory + parameters['retrieved_data_folder']

#the ML tasks and models
task_models = task_parameters

#prefixes for retrieving data through the sparql endpoint
prefixes = parameters['prefixes']
#sparql endpoint and login details
sparql_endpoint = parameters['sparql_endpoint']
username = parameters['username']
password = parameters['password']
