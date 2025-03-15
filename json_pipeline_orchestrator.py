import string
import config
import random

#receives policy from intent compiler with task classification
#selects model arbitrarily
#generates pre- and post-conditions from UPC annotations in IKB or a local function store
#combines the task, model and conditions to get json pipeline
#sends pipeline to runtime layer
tasks_models = config.task_models
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
def json_pipeline_orchestrator_fun(policy):
    model_name = random.choice(tasks_models[policy["task"]])
    pipeline = {
        "data": policy["data"],
        "task": "",
        "task_description": {
            "training": "",
            "inference": {
                "infer": "",
                "model_name": ""
            },
            "save_model": ""
        },
        "model": model_name,
        "target": policy["target"],
        "specific_columns": policy["specific_columns"],
        "test_fraction": 0.2,
        "scaling_bounds": [-1, 1],
        "pre-conditions": [],
        "post-conditions": [],
        "pipeline_id": ""
    }
    '''if data is numerical and policy["task"] == "classification":
        pipeline["task"] = "num_classification"
    elif data is not numerical and policy["task"] == "classification":
        pipeline["task"] = "text_classification"'''
    #get pre and post conditions from UPC IKB annotations

    if "training" in policy["execution_type"]:
        pipeline["task_description"]["training"] = "yes"
        pipeline["task_description"]["save_model"] = policy["training"]["save_model"]
    if "inference" in policy["execution_type"]:
        pipeline["task_description"]["inference"]["infer"] = "yes"
        pipeline["task_description"]["inference"]["model_name"] = policy["inference"]["inference_saved_model"]

    pipeline["pre-conditions"] = "UPC preconditions"
    pipeline["post-conditions"] = "UPC postconditions"

    id_digits = 9
    charset = string.ascii_uppercase + string.digits
    pipeline_id = ''.join(random.choices(charset, k=id_digits))
    pipeline["pipeline_id"] = pipeline_id
    print("pipeline: ", pipeline)
    return pipeline

#json_pipeline_orchestrator_fun(intent["fields"])