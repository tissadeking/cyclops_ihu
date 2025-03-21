import requests
import json

#script to send intents

#API endpoint for sending intents
url = "http://127.0.0.1:5002/intent"

#exploratory intent
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
'''

#analytical intent
#df = pd.read_csv("policy_store.csv")
intent = {
    "intent_type": "analytical",
    "fields": {
        "data": ["reference to dataframe 1", "dataframe 2", "...."],
        "task": "classification",
        "execution_type": ["training", "inference"],
        "target": "target variable",
        "specific_columns": ["feature 1", "feature 2", "feature 3"],
        "preprocessing_choice": "reshuffle the dataset",
        "training": {
            "save_model": "yes/no",
        },
        "inference": {
            "inference_saved_model": "name of model to use for inference",
        },
        "clustering": {
            "cluster_feature": "name of feature to perform clustering on",
        },
        "anomaly_detection": {
            "old_data": "reference to old data",
            "new_data": "reference to new data"
        },
        "query": "summary of the query",
        "intent_id": "XGTHSU45",
        "userid": "!!06!E85QWE2VBJ6NNLV"
    }

}

# Convert dictionary to JSON
headers = {"Content-Type": "application/json"}
response = requests.put(url, data=json.dumps(intent), headers=headers)
#print(response)
# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())
