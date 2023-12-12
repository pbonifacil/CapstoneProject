import pandas as pd
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents.agent_toolkits.conversational_retrieval.tool import (
    create_retriever_tool,
)
from langchain.memory import ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.tools import PythonAstREPLTool
from langchain.vectorstores import FAISS
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TEMPLATE = """You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
It is important to understand the attributes of the dataframe before working with it. This is the result of running `df.head().to_markdown()`

<df>
{dhead}
</df>

You are not meant to use only these rows to answer questions - they are meant as a way of telling you about the shape and schema of the dataframe.
You also do not have to use only the information here to answer questions - you can run intermediate queries to do exploratory data analysis to give you more information as needed.

You have a tool called `car_model_search` through which you can lookup car listings by the car's brand and model name and find the records corresponding to cars with similar name as the query.
You should only really use this if your search term contains ONLY the car brand and car model. Otherwise, try to solve it with code.

For example:

<div>
<question>Find me 1 BMW X2.</question>
<logic>Use `car_model_search` since you can use the query `BMW X2`</logic>

<question>Find me 1 red car bellow 10000 euros.</question>
<logic>Use `python_repl` since even though the question is about a car, you don't know the exact model so you can't include it.</logic>
</div>

<div>
RESTRICTIONS:
<tool>python_repl</tool>
<restriction>When querying the dataset ALWAYS use .sample(1)</restriction>
</div>
"""


class PythonInputs(BaseModel):
    query: str = Field(description="code snippet to run")


def get_chain():
    pd.set_option("display.max_rows", 20)
    pd.set_option("display.max_columns", 21)

    path = "webscrapers/car_dataset_small.csv"

    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("car_dataset_small", embedding_model)
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(), "car_model_search", "Search for a car model by name"
    )

    df = pd.read_csv(path, index_col=0)
    template = TEMPLATE.format(dhead=df.head().to_markdown())

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
            ("human", "{input}"),
        ]
    )

    repl = PythonAstREPLTool(
        locals={"df": df},
        name="python_repl",
        description="Runs code and returns the output of the final line",
        args_schema=PythonInputs,
    )
    tools = [repl, retriever_tool]
    agent = OpenAIFunctionsAgent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"), prompt=prompt, tools=tools
    )

    memory = ConversationTokenBufferMemory(llm=ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo"), max_token_limit=100)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, max_iterations=2, early_stopping_method="generate", memory=memory, verbose=False
    )
    return agent_executor

# Use agent('question') to run the agent
