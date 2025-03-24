from retrieve_data import retrieve_data_fun
import pandas as pd, config
from data_retriever import data_retriever_fun
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
    #Just for testing, the real functionality is highlighted above and implemented by the function below
    #df = pd.read_csv('policy_store.csv')
    #df = pd.read_csv(config.policy_store_directory)

    #real functionality of generating sparql queries from lists of classes and properties
    def generate_sparql_queries(query_list, prefixes):
        """
        Generates a list of SPARQL queries
        """
        queries = []
        for query_dict in query_list:
            for class_name, property_name in query_dict.items():
                query_prefixes = "\n".join([f"PREFIX {p}: <{uri}>" for p, uri in prefixes.items()])
                selected_variables = []
                query_body = ""
                class_variable = class_name.lower()

                for prefix, uri in prefixes.items():
                    query_body += f"  ?{class_variable} a {prefix}:{class_name} ;\n"
                    query_body += f"          {prefix}:{property_name} ?{property_name.lower()} .\n"
                    selected_variables.append(f"?{property_name.lower()}")
                    break

                query = f"""
                {query_prefixes}
                SELECT ?{class_variable} {' '.join(selected_variables)}
                WHERE {{
                {query_body}
                }}
                """.strip()
                queries.append(query)
        #for q in queries:
        #    print(q, "\n")
        #call the function to query the endpoint with the generated queries straight up
        return data_retriever_fun(queries)

    #gets the prefixes from the config.yml file
    prefixes = config.prefixes
    #calls the function to generate sparql queries which also implements the querying
    df = generate_sparql_queries(policy['query_list'], prefixes)
    return retrieve_data_fun(df, policy['intent_id'], policy['userid'], policy['query'])