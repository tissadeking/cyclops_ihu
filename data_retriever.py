from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd, config

def execute_sparql_queries(queries, endpoint, username, password):
    """
    Executes a list of SPARQL queries against the endpoint and collects results.
    """
    data_list = []
    for query in queries:
        sparql = SPARQLWrapper(endpoint)
        sparql.setCredentials(username, password)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            results = sparql.query().convert()
            if results["results"]["bindings"]:
                data_list.extend(results["results"]["bindings"])
        except Exception:
            continue  # Skip if query fails
    return data_list

def merge_data(data_list):
    """
    Merges the retrieved data into a single structure.
    """
    merged_data = {}
    for data in data_list:
        for key, value in data.items():
            if key not in merged_data:
                merged_data[key] = []
            merged_data[key].append(value["value"])
    return merged_data

# Example usage
'''query_list = [
    {'Notice': 'hasPublicationDate'},
    {'Notice': 'hasDispatchDate'},
    {'Contract': 'publisher'}
]

prefixes = {
    "epo": "http://data.europa.eu/a4g/ontology#",
    "dct": "http://purl.org/dc/terms/"
}'''

'''sparql_endpoint = "https://cyclops-dev.ontopic.dev/sparql-endpoint/uc3-mitender/sparql"
username = "tubs"
password = "RenfeokKinlaJis"'''

sparql_endpoint = config.sparql_endpoint
username = config.username
password = config.password

#queries = generate_sparql_queries(query_list, prefixes, sparql_endpoint, username, password)
def data_retriever_fun(queries):
    data_list = execute_sparql_queries(queries, sparql_endpoint, username, password)
    #merged_data = merge_data(data_list)
    #print(merged_data)
    print(data_list)
    new_data_list = []
    for data in data_list:
        for key in list(data.keys()):
            data[key] = data[key]['value']
        new_data_list.append(data)
    print(new_data_list)
    data = pd.DataFrame(new_data_list)
    print(data)
    return data