from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

messages = [
    SystemMessage(content="You are a helpful assistant that can answer questions and help with tasks."),
    HumanMessage(content="What is the capital of France?"),
    AIMessage(content="Paris."),
    HumanMessage(content="What is the capital of Germany?"),
]

res = llm.invoke(messages)
print(res.content)


# Alternative models

