#receive data that is generated
#save in data folder
#call retrieve function
import os, json, config
from sql_func import insert_data_store, delete_data_store

#convert df to string
def convert_df_to_text(df):
    return df.to_string(index=False)

#parse data sent as dataframe by the sparql generator
def retrieve_data_fun(df, intent_id, userid):
    file_path = config.retrieved_data_directory
    #save data to retrieved_data.txt inside data_folder
    df.to_json(file_path)
    #extract cols of data
    data_cols = df.columns.tolist()
    data_cols = json.dumps(data_cols)
    #convert data to json
    df_json = df.to_json()
    if df_json != {}:
        #delete existing entry in the data store with the same user id and intent id with incoming user id and intent id
        delete_data_store(userid, intent_id)
        #save the new entry to the data store with user id, intent id, data in json and columns
        insert_data_store(userid, intent_id, df_json, data_cols)

    return userid, intent_id, df_json, data_cols


