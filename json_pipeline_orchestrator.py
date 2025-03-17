import string
import pandas as pd
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
        #"data": [pd.read_csv('policy_store.csv'), "dataframe 2", "...."],
        "data": ["dataframe 1", "dataframe 2", "...."],
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
#generates pipeline from the received policy
def json_pipeline_orchestrator_fun(policy):
    #currently chooses model randomly from the lists
    #in IT-2, AI Marketplace would do this
    model_name = random.choice(tasks_models[policy["task"]])
    post_conditions = []
    #initial pipeline definition
    pipeline = {
        "data": policy["data"][0],
        "task": policy["task"],
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
        "test_fraction": policy["test_fraction"],
        "scaling_bounds": policy["scaling_bounds"],
        "pre-conditions": [],
        "post-conditions": [],
        "pipeline_id": ""
    }

    #decide training and inference
    if "training" in policy["execution_type"]:
        pipeline["task_description"]["training"] = "yes"
        #choose to save a model after training
        pipeline["task_description"]["save_model"] = policy["training"]["save_model"]
    if "inference" in policy["execution_type"]:
        pipeline["task_description"]["inference"]["infer"] = "yes"
        #get model_name for inference
        pipeline["task_description"]["inference"]["model_name"] = policy["inference"]["inference_saved_model"]

    #define pre-conditions
    #pre-conditions are what need to be done to the data before model training
    #these pre-conditions are already defined in the pipeline_executor
    #the pipeline_executor is not part of the software here
    if pipeline["task"] == "num_classification":
        pipeline["pre-conditions"] = ["encode_target", "convert_np_array",
            "train_split"]
    if pipeline["task"] == "text_classification":
        pipeline["pre-conditions"] = ["combine_text_data", "extract_x_y_text",
            "train_split"]
    if pipeline["task"] == "text_classification_cross_val":
        pipeline["pre-conditions"] = ["combine_text_data", "extract_x_y_text",
            "train_split"]
    if pipeline["task"] == "regression":
        pipeline["pre-conditions"] = ["extract_x_y", "train_split"]
    #if pipeline["task"] == "time_series_forecasting":

    #define post-conditions
    # post-conditions are what need to be done after model training
    # these post-conditions are also defined in the pipeline_executor
    if pipeline["task_description"]["save_model"] == "yes":
        post_conditions.append("save_model")
    if pipeline["task_description"]["training"] == "yes":
        if policy["task"] == "classification":
            post_conditions.append("get_metrics_class")
        elif policy["task"] == "regression":
            post_conditions.append("get_metrics_reg")
        elif policy["task"] == "time_series_forecasting" and policy["model"] != "var":
            post_conditions.append("get_metrics_forecast_fun")
        elif policy["task"] == "time_series_forecasting" and policy["model"] == "var":
            post_conditions.append("get_metrics_var_forecast_fun")

    #complete pre-conditions definition
    if pipeline["task"] == "time_series_forecasting" and \
        "get_metrics_forecast_fun" in post_conditions:
            pipeline["pre-conditions"] = ["extract_x_y", "train_split"]

    #OR
    # get pre and post conditions from UPC IKB annotations
    #pipeline["pre-conditions"] = "UPC preconditions"
    #pipeline["post-conditions"] = "UPC postconditions"

    #generate pipeline ID
    id_digits = 9
    charset = string.ascii_uppercase + string.digits
    pipeline_id = ''.join(random.choices(charset, k=id_digits))
    pipeline["pipeline_id"] = pipeline_id
    print("pipeline: ", pipeline)

    #TO CHANGE BACK TO DATAFRAME LATER
    pipeline["data"] = "data"
    return pipeline

#json_pipeline_orchestrator_fun(intent["fields"])