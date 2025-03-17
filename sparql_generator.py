from retrieve_data import retrieve_data_fun
import pandas as pd, config

#receives policy from intent compiler
#the policy contains query list
#the query list is a list of most related queries
#the sparql generator uses the query list to query the endpoint
#it then gets a list containing the corresponding dataframes or a single dataframe
#and calls the retrieve_data function with arg as the df, user id and intent id

'''policy = {
    'data': 'public procurement', 
    'intent_id': '98HTS738HD', 
    'query_list': [
        {
            'notice': 'hasPublicationDate'
        }, 
        {
            'contract': 'hasTitle'
        }, 
        {
            'location': 'hasNutsCode'
        }, 
        {
            'organization': 'hasMainActivity'
        }, 
        {
            'organization': 'hasLegalName'
        }
    ], 
    'userid': '339CKZDS16!WE8HA3Q.6'
}'''

def sparql_generator_fun(policy):
    #Just for testing, the real functionality is highlighted above
    #df = pd.read_csv('policy_store.csv')
    df = pd.read_csv(config.policy_store_directory)
    return retrieve_data_fun(df, policy['intent_id'], policy['userid'])