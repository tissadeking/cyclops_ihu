import yaml

files_directory = '/app/'
yml_file = 'config.yml'
with open(yml_file) as f:
    parameters = yaml.safe_load(f)
    #print("yml accessed and opened")

tasks_models_file = 'tasks_models.yml'
with open(tasks_models_file) as f:
    task_parameters = yaml.safe_load(f)
    #print("tasks yml accessed and opened")

groq_api_key = parameters['groq_api_key']
host = parameters['host']
port = parameters['port']
dc_port = parameters['dc_port']

policy_store_directory = files_directory + parameters['policy_store_file']
current_user_directory = files_directory + parameters['current_user_file']
processed_data_directory = files_directory + parameters['processed_data_file']
retrieved_data_directory = files_directory + parameters['retrieved_data_file']
retrieved_data_folder = files_directory + parameters['retrieved_data_folder']

task_models = task_parameters
