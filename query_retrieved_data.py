from langchain_openai import ChatOpenAI
import config, logging

#initialize model
groq_api_key = config.groq_api_key
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama3-8b-8192"
                    )

#query the retrieved data
def llm_query_fun_3_8(user_query, data):
    def query_dataset(user_query):
        prompt = f"""
        You are a data analyst. Given the following dataset, answer the user's query. Please, avoid mistakes.
        Answer only according to information you find in the dataset. If an information is not found in the dataset just say you don't know and stop there.

        Dataset:
        {data}

        User Query:
        "{user_query}"

        Return the answer in plain text.
        """
        response = llama3.invoke(prompt)

        return response.content
    answer = query_dataset(user_query)
    #logging.info("logged answer to query: ", answer)
    #print("answer to query: ", answer)
    return answer

#query = "explain the class in the dataset"
#llm_query_fun_3_8(query)