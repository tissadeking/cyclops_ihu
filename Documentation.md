# Documentation for Intent-Based Human Interface (CyclOps)

This repository contains some not all of the components in the CyclOps Intent-based Human Interface (IHU). This is only the TUBS IHU Part. The components from the other partners which are NLP Chat and Info Retrievel are not here. The essence of this file is to help any person working on the codes to understand what blocks of codes fulfill what functionalities.
The parameters of the software are stored in the config.yml and are accessed by the config.py file which enables other scripts to use them through "import config".

The SQL database and the tables: users and data_store are created automatically at the start of the software through the script init.sql.

## Identity and Session Management
- This functionality is only part of the IHU on a temporal basis, in IT-2 another module will be in charge of it.
- When a user creates an account through the GUI by submitting the button after putting in their username, email and password, the function *register_fun* in main.py is called.
- This function takes in the user details and uses the functions *check_email* and *check_username* which are inside the file sql_func.py to check whether the email and/or the username already exists, if that's the case then the registration would not proceed. If not, the function creates a unique user ID and then stores the email, username, password and user ID inside the users table in the SQL database using the function *insert_data* also in the file sql_func.py.
- Whenever a user logs in through the GUI, the function *login_fun* in main.py is called. The function checks whether username and password are valid through the function *check_data* found in sql_func.py. If they are valid, it redirects the user to the NLP Chat through: f"https://chat.datacalculus.net/?userID={userid}".
- The userid variable is attached to the URL whenever a new instance of the NLP Chat is loaded up for the user so that all the activities of the user would be assigned to their userid for session management.
 
## Workflow 1 - Exploratory Workflow
- This workflow involves the processing of exploratory intents which are simply user queries on CyclOps datasets.
- It starts with the TUBS IHU Part receiving structured intents as put requests from the Info Retrieval through the intent API endpoint set up in main.py and the function *update_field* still in main.py.
- The function then sends the received intents to the function *intent_compiler_fun* in intent_compiler.py.
- *intent_compiler_fun* first creates a list of key-value combinations of the fields in the intents. This list is referred to as extract_list.
- Then it reads the data from the policy store found in policy_store.csv, picks the class_description_list which is a list of the descriptions of the various classes in the policy store. It does same for the property_description_list which is a list of the descriptions of the various properties in the policy store.
- For each key-value combination in the extract_list, the function calls *match_llm_zero* function within match_policies.py to use Large Language Models (LLM) to find the best class_description from the class_description_list that matches the key-value combination, it adds its corresponding class to a query_class_list it created.
- It does same with the property_description_list and finds the best property_description that matches the key-value combination, and adds its corresponding property to a query_property_list it created.
- A combination of each class in the query_class_list as key and a property in the query_property_list as value gives a query_dict. All possible query_dicts are added to a query_list.
- The query_list plus the userid, intentid and the data makes the policy.
- Back in main.py, the function *update_field* passes the policy to the function *sparql_generator_fun* in sparql_generator.py.
- The function *sparql_generator_fun* first generates sparql queries with the policy using the function *generate_sparql_queries* within the same *sparql_generator_fun*. After which it sends the generated queries to the function *data_retriever_fun* which is inside data_retriever.py. 
- *data_retriever_fun* uses the function *execute_sparql_queries* also found in the same script to query the sparql endpoint of IKB defined in the config.yml file. It retrieves this data afterwards in the form of a dataframe.
- The data is sent to the function *retrieve_data_fun* in retrieve_data.py by *sparql_generator_fun* in sparql_generator.py.
- *retrieve_data_fun* then stores the data with userid and intentid inside the data_store with the functions *delete_data_store* and *insert_data_store* both found in sql_func.py, and also converts it to csv file and stores it inside the long-term storage minio bucket through the functions *ensure_bucket* and *create_object* both found in minio_crud.py.
- The function *retrieve_data_fun* also tries to query the retrieved data with the function *llm_query_fun_3_8* written in query_retrieved_data.py. If the query goes successful then it returns the userid, intentid, answer to the query and columns of the data as output. However, if the query doesn't work, it returns the userid, intentid, json format of the data and columns of the data as output, but only the first three parameters are selected as parts of the answer by the funtion *update_field* in main.py.
- After everything, the answer is sent as a post request to the NLP Chat API endpoint "https://chatapi.datacalculus.net/receive-request" by the same function *update_field* in main.py

 
## Workflow 2 - Analytical Workflow
- This workflow involves the processing of analytical intents which are requests for generation of data analytics pipelines to be executed with CyclOps datasets.
- It starts with the TUBS IHU Part receiving structured intents as put requests from the Info Retrieval through the intent API endpoint set up in main.py and the function *update_field* still in main.py.
- The function then sends the received intents to the function *intent_compiler_fun_2* in intent_compiler.py.
- *intent_compiler_fun_2* adds missing fields like scaling_bounds, test_fraction, etc, and also groups the task if it's classification into numerical or text classification based on how the data in question is. It retrieves the data from the long-term storage on minio using the object name contained in the data field of the intent. The object name is currently a combination of userid and exploratory intentid. 
- After that, it sends the policy to the function *json_pipeline_orchestrator_fun* inside json_pipeline_orchestrator.py.
- *json_pipeline_orchestrator_fun* generates the pipeline needed to fulfill the user request by defining the model to use, assigning the pre- and post-conditions based on the task, and creating a unique ID for the pipeline.
- After everything, the pipeline is returned or sent as a post request to the Runtime Layer API endpoint by the function *update_field* in main.py


