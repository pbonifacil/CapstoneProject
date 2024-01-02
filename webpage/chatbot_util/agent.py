import pandas as pd
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents.agent_toolkits.conversational_retrieval.tool import (
    create_retriever_tool,
)
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.tools import PythonAstREPLTool
from langchain.vectorstores import FAISS
from pydantic import BaseModel, Field
try:
    from .template import TEMPLATE
except ImportError:
    from template import TEMPLATE
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class PythonInputs(BaseModel):
    query: str = Field(description="code snippet to run")


def get_chain(path):
    pd.set_option("display.max_rows", 20)
    pd.set_option("display.max_columns", 21)

    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("./chatbot_util/car_dataset_small", embedding_model)
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(), "car_model_search", "Search for a car model by name"
    )

    df = pd.read_csv(path, index_col=0)
    template = TEMPLATE.format(dcolumns=str(list(df.columns)),
                               dfadvertiser=str(list(df.Advertiser.unique())),
                               dfbrand=str(list(df.Brand.unique())),
                               dffuel=str(list(df.Fuel.unique())),
                               dfsegment=str(list(df.Segment.unique())),
                               dfcolor=str(list(df.Color.unique())),
                               dfgeartype=str(list(df.Gear_Type.unique())),
                               dfcondition=str(list(df.Condition.unique())),
                               dfcomparedprice=str(list(df.Compared_Price.unique())))

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="chat_history"),
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

    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)

    agent = OpenAIFunctionsAgent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"), prompt=prompt, tools=tools, verbose=True
    )

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, max_iterations=2, early_stopping_method="generate", verbose=True, memory=memory, handle_parsing_errors=True
    )
    return agent_executor


class AutoMentorChatbot:
    def __init__(self, path):
        self.agent = get_chain(path)
        self.chat_history = []

    def generate_response(self, message: str):
        return self.agent(message)

    def __str__(self):
        class_name = str(type(self)).split('.')[-1].replace("'>", "")
        return f"🤖 {class_name}."


#agent = get_chain('car_dataset.csv')
