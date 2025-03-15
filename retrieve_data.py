#receive data that is generated
#save in data folder
#call retrieve function
import os, json, config
from sql_func import insert_data_store, delete_data_store

def convert_df_to_text(df):
    return df.to_string(index=False)

def retrieve_data_fun(df, intent_id, userid):
    file_path = config.retrieved_data_directory
    df.to_json(file_path)
    data_cols = df.columns.tolist()
    data_cols = json.dumps(data_cols)
    df_json = df.to_json()
    delete_data_store(userid, intent_id)
    insert_data_store(userid, intent_id, df_json, data_cols)

    return userid, intent_id, df_json, data_cols
