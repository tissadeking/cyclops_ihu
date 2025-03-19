from llama_index.llms.groq import Groq
from langchain_openai import ChatOpenAI
import json
import config

# Initialize Groq model
groq_api_key = config.groq_api_key
model = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama3-8b-8192",
                    )

#Convert dictionary and dataFrame to text
def convert_dict_to_text(df):
    return str(df)
def convert_df_to_text(df):
    return df.to_string(index=False)

#to match pair of key and value retrieved during intent compilation with most suitable class
#it does same for most suitable property
def get_prompt(df1, ref_description):
    df1_text = convert_dict_to_text(df1)
    ref_description = convert_dict_to_text(ref_description)

    f'''prompt = f"""
    extract:
    {df1_text}

    Reference description list:
    {ref_description}

    Please analyze the text: df1_text and the list: ref_description and determine the item inside the ref_description that matches best with df1_text.
    Please, don't add any explanations, just write that JSON output.
    """'''
    prompt = """Please, don't add any summary or explanations, just put a json output.
    Check the data in the text: """ + df1_text + """ and find its best match in the reference data """ + ref_description + """. 
    Respond with a JSON that will have key: 'answer' and value as the chosen match.
    Don't add any term that is not from the ref_description. If a parameter is not found, just ignore it.
    Please, don't add any summary or explanation, just give the json output.
    Don't write anything like '''json in the output, just write only the output itself.
    """
    return prompt

#function to send the prompt to LLM
def match_with_groq(prompt):
    response = llama3.invoke(prompt)
    return response.content

#call the functions above and output the result as json
def match_llm_zero(df1, ref):
    prompt = get_prompt(df1, ref)
    result = match_with_groq(prompt)
    #result = json.loads(result)
    try:
        result = json.loads(result)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return None
    return result