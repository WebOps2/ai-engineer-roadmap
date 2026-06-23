from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

messages = [
    SystemMessage(content="You are a helpful assistant that can answer questions and help with tasks."),
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        break
    messages.append(HumanMessage(content=user_input))
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print(f"Assistant: {response.content}")
    
    
print("Goodbye!")
print(messages)