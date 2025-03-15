import pandas as pd, config
from match_policies import match_llm_zero
from json_pipeline_orchestrator import json_pipeline_orchestrator_fun

df = pd.read_csv(config.policy_store_directory)

class_list = df['class'].tolist()
class_description_list = df['class_description'].tolist()
property_list = df['property'].tolist()
property_description_list = df['property_description'].tolist()

def intent_compiler_fun(fields):
    extract_list = []
    for key in list(fields.keys()):
        if key != 'data' and key != 'query':
            if type(fields[key]) == dict:
                for key_2d in list(fields[key].keys()):
                    if fields[key][key_2d] != "":
                        key_2d_dict = {}
                        key_join = key + '_' + key_2d
                        key_2d_dict[key_join] = fields[key][key_2d]
                        extract_list.append(key_2d_dict)
            else:
                if fields[key] != "" and fields[key] != []:
                    key_dict = {}
                    key_dict[key] = fields[key]
                    extract_list.append(key_dict)
    #print(extract_list)

    query_class_list = []
    query_property_list = []

    for extract in extract_list:
        #use class description to find class in class_list that matches best with extract
        #add class to query_class_list
        class_description = match_llm_zero(extract, class_description_list)["answer"]
        try:
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
        property_description = match_llm_zero(extract, property_description_list)["answer"]
        #print('prop description: ', property_description)
        try:
            property_ind = property_description_list.index(property_description)
            property_name = property_list[property_ind]
            if property_name not in query_property_list:
                query_property_list.append(property_name)
        except:
            continue


    #print('query property list: ', query_property_list)
    #print('query class list: ', query_class_list)
    query_list = []
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

    policy = {}
    policy['data'] = fields['data']
    policy['query_list'] = query_list
    policy['intent_id'] = fields['intent_id']
    policy['userid'] = fields['userid']
    #logging.info("policy: ", policy)
    print('policy: ', policy)
    return policy

def intent_compiler_fun_2(intent):
    return json_pipeline_orchestrator_fun(intent)








