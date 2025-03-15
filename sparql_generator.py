from retrieve_data import retrieve_data_fun
import pandas as pd, config

#receives policy from intent compiler
#the policy contains query list
#the query list is a list of most related queries
#the sparql generator uses the query list to query the endpoint
#it then gets a list containing the corresponding dataframes
#and calls the retrieve_data function with arg as the list of dfs


def sparql_generator_fun(policy):
    #Just for testing, the real functionality is highlighted above
    #df = pd.read_csv('policy_store.csv')
    df = pd.read_csv(config.policy_store_directory)
    return retrieve_data_fun(df, policy['intent_id'], policy['userid'])