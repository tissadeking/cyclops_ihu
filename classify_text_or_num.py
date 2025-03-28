import pandas as pd

#function to group classification task as text or numerical classification
def classify_task(df, cols):
    #df is the dataframe
    # Identify numerical and text columns in the given column list
    numerical_cols = [col for col in cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    text_cols = [col for col in cols if col in df.columns and pd.api.types.is_string_dtype(df[col])]
    # Classification rule
    #if all cols are numerical
    if len(numerical_cols) == len(cols):
        task_type = "num_classification"
    else:
        task_type = "text_classification"
        # Convert numerical columns to strings
        df[numerical_cols] = df[numerical_cols].astype(str)
    '''# Classification rule
    if text_cols:  # If at least one text column exists
        task_type = "text_classification"
        # Convert numerical columns to strings
        df[numerical_cols] = df[numerical_cols].astype(str)
    else:  # If no text columns, classify as numerical classification
        task_type = "num_classification"'''

    return task_type, df


