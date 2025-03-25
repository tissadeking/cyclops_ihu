#receive data that is generated
#save in data folder
#call retrieve function
import os, json, config
from minio_crud import create_object, ensure_bucket
from sql_func import insert_data_store, delete_data_store
from query_retrieved_data import llm_query_fun_3_8

#convert df to string
def convert_df_to_text(df):
    return df.to_string(index=False)

#parse data sent as dataframe by the sparql generator
def retrieve_data_fun(df, intent_id, userid, query):
    global answer
    file_path = config.retrieved_data_directory
    #save data to retrieved_data.txt inside data_folder
    df.to_json(file_path)
    #extract cols of data
    data_cols = df.columns.tolist()
    data_cols = json.dumps(data_cols)
    #convert data to json
    #df_json = df.to_json()
    df_json = df.to_json(orient="columns", force_ascii=False)
    df_json = df_json.replace("\\/", "/")
    if df_json != {}:
        #delete existing entry in the data store with the same user id and intent id with incoming user id and intent id
        delete_data_store(userid, intent_id)
        #save the new entry to the data store with user id, intent id, data in json and columns
        insert_data_store(userid, intent_id, df_json, data_cols)

        # To store data in long-term storage (minio object store)
        # Example object details
        object_name = userid + '_' + intent_id
        #write data to csv
        csv_name = intent_id + '.csv'
        df.to_csv(csv_name, index=False)
        upload_path = csv_name
        #ensure bucket is available
        ensure_bucket()
        #create the object inside the bucket in minio
        create_object(object_name, upload_path)
        # delete the uploaded csv file as it's not needed anymore
        if (os.path.exists(csv_name) and os.path.isfile(csv_name)):
            os.remove(csv_name)
    #converts the df to text before querying
    df_text = convert_df_to_text(df)
    try:
        #query the retrieved data
        answer = llm_query_fun_3_8(query, df_text)
        #answer = df_json
        #answer = json.loads(answer)
    except:
        #if it doesn't work return the data as a json
        answer = df_json

    return userid, intent_id, answer, data_cols
    #return userid, intent_id, df_json, data_cols


