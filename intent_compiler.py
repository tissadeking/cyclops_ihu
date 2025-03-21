import pandas as pd, config
from match_policies import match_llm_zero
from json_pipeline_orchestrator import json_pipeline_orchestrator_fun
from classify_text_or_num import classify_task
#from match_policies_tfidf import match_tfidf

#read the policy store into a dataframe
#df = pd.read_csv('policy_store.csv')
df = pd.read_csv(config.policy_store_directory)

#create lists for the different columns of the policy store
class_list = df['class'].tolist()
class_description_list = df['class_description'].tolist()
property_list = df['property'].tolist()
property_description_list = df['property_description'].tolist()

#compilation of exploratory intents
def intent_compiler_fun(fields):
    #fields here is the exploratory intent received by the compiler
    extract_list = []
    #extract key-value pairs of the fields into extract_list
    for key in list(fields.keys()):
        if key != 'data' and key != 'query':
            if type(fields[key]) == dict:
                for key_2d in list(fields[key].keys()):
                    #for values that are also dicts, join the key and value for each entry
                    #what to extract would be the key:joined key and value above
                    if fields[key][key_2d] != "":
                        key_2d_dict = {}
                        key_join = key + '_' + key_2d
                        key_2d_dict[key_join] = fields[key][key_2d]
                        extract_list.append(key_2d_dict)
            else:
                #for values that are not dicts, simply append key:value to extract_list
                if fields[key] != "" and fields[key] != []:
                    key_dict = {}
                    key_dict[key] = fields[key]
                    extract_list.append(key_dict)
    #print(extract_list)

    query_class_list = []
    query_property_list = []

    for extract in extract_list:
        #extract is a combination of key and value from the fields above
        #use class description to find class in class_list that matches best with extract
        #add class to query_class_list
        #got to file match_llm_zero to see how the matching is done
        #class_description = match_tfidf(extract, class_description_list)["answer"]
        #class_description = match_tfidf(extract, class_description_list)
        try:
            class_description = match_llm_zero(extract, class_description_list)["answer"]
            #class_description = match_tfidf(extract, class_description_list)["answer"]
            #print('class descr: ', class_description)
            class_ind = class_description_list.index(class_description)
            class_name = class_list[class_ind]
            if class_name not in query_class_list:
                query_class_list.append(class_name)
        except:
            continue
    #print(property_list)
    #print(property_description_list)
    for extract in extract_list:
        # use property description to find property in property_list that matches best with extract
        # add property to query_property_list
        #property_description = match_tfidf(extract, property_description_list)["answer"]
        #property_description = match_tfidf(extract, property_description_list)
        try:
            property_description = match_llm_zero(extract, property_description_list)["answer"]
            #print('prop description: ', property_description)
            #property_description = match_tfidf(extract, property_description_list)["answer"]
            property_ind = property_description_list.index(property_description)
            property_name = property_list[property_ind]
            if property_name not in query_property_list:
                query_property_list.append(property_name)
        except:
            continue


    #print('query property list: ', query_property_list)
    #print('query class list: ', query_class_list)
    query_list = []
    #generate combinations of class and property found in query_class_list and query_property_list
    for query_class in query_class_list:
        # Filter the DataFrame based on query class and data as procurement
        filtered_df = df[(df['class'] == query_class) & (df['data'] == fields['data'])]
        # Extract the 'property' column
        property_values = filtered_df['property'].tolist()
        for query_property in query_property_list:
            if query_property in property_values:
                query_dict = {}
                query_dict[query_class] = query_property
                query_list.append(query_dict)

    #print('query list: ', query_list)

    #create policy that contains these combinations of class and property
    #a combination of class and property is what the exploratory analysis engine needs to generate a SPARQL query
    policy = {}
    policy['data'] = fields['data']
    policy['query_list'] = query_list
    policy['intent_id'] = fields['intent_id']
    policy['userid'] = fields['userid']
    #logging.info("policy: ", policy)
    print('policy: ', policy)
    return policy

#compilation of analytical intents
def intent_compiler_fun_2(intent):
    #test_fraction is the ratio of test to train data during train_test_split
    intent["test_fraction"] = 0.2
    #scaling bounds is the boundary for scaling of values in a column of a dataframe
    #this is useful if the column values are to be scaled
    intent["scaling_bounds"] = [-1, 1]

    # classify as text or num classification when task received in intent is classification
    if intent["task"] == "classification":
        #get list of data columns
        #cols = intent["data"][0].columns.tolist()
        #TO BE CHANGED TO IMPLEMENTATION WITH INTENT ID AND STORED DATA LATER
        df = pd.read_csv(config.policy_store_directory)
        cols = df.columns.tolist()
        #however, if user had defined columns they want, use theirs instead
        if intent["specific_columns"] != "":
            cols = intent["specific_columns"]
        # TO BE CHANGED TO IMPLEMENTATION WITH INTENT ID AND STORED DATA LATER
        #task_type, df = classify_task(intent["data"][0], cols)
        task_type, df = classify_task(df, cols)
        #task_type is num_classification or text_classification
        intent["task"] = task_type
        intent["data"][0] = df
    #send the parsed intent as policy to pipeline orchestrator
    return json_pipeline_orchestrator_fun(intent)


'''intent = {
    "intent_type": "exploratory",
    "fields": {
        "data": "public procurement",
        "parameter": "notices",
        "aggregate": "count",
        "description": {
            "event": "",
            "reference": "",
            "sentiment": ""
        },
        "entity": "",
        "constraints": [],
        "influence": {
            "cause": "",
            "effect": ""
        },
        "location": {
            "main_location": "Europe",
            "specific_location": ""
        },
        "time": "last year",
        "query": "get the notices in Europe last year",
        "intent_id": "98HTS738HD",
        "userid": "!!06!E85QWE2VBJ6NNLV"
    }
}
intent_compiler_fun(intent['fields'])'''







