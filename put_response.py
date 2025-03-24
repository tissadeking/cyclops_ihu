import requests
import json

#script to send intents

#API endpoint for sending intents
url = "http://127.0.0.1:5002/intent"

#exploratory intent
intent = {
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
        "intent_id": "5GDHT67S8S",
        "userid": "Y8H!!!SU9A97DJJKSDFS"
    }
}
'''

#analytical intent
#df = pd.read_csv("policy_store.csv")
intent = {
    "intent_type": "analytical",
    "fields": {
        "data": ["Y8H!!!SU9A97DJJKSDFS_5GDHT67S8S", "dataframe 2", "...."],
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
        "userid": "Y8H!!!SU9A97DJJKSDFS"
    }

}
'''

'''from minio import Minio
minio_endpoint = "localhost:9100"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "long-term"
#file_path = "policy_store.csv"
#download_path = "policy_store_downloaded.csv"

print(minio_endpoint, access_key, secret_key, bucket_name)

# Initialize MinIO client
minio_client = Minio(
    minio_endpoint,  # Replace with your MinIO server URL
    access_key=access_key,  # Replace with your MinIO access key
    secret_key=secret_key,  # Replace with your MinIO secret key
    secure=False  # Set to False if not using HTTPS
)

#client = Minio("minio:9000", "your-access-key", "your-secret-key", secure=False)
print(minio_client.list_buckets())  # This should return a list of buckets'''

# Convert dictionary to JSON
headers = {"Content-Type": "application/json"}
response = requests.put(url, data=json.dumps(intent), headers=headers)
#print(response)
# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())
