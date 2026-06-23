from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

# template = "Write a {tone} email to {recipient} about {topic}."

# prompt_template = ChatPromptTemplate.from_template(template)

# prompt = prompt_template.invoke({"tone": "formal", "recipient": "John", "topic": "the weather"})


# res = llm.invoke(prompt)
# print(res.content)


# Example 2: Prompt with system and user messages   

messages = [
    ("system", "You are a helpful assistant that can answer questions about {club_name}."),
    ("user", "What year was {club_name} founded?"),
]
    

prompt_template = ChatPromptTemplate.from_messages(messages)

prompt = prompt_template.invoke({"club_name": "Arsenal"})
print(prompt)

res = llm.invoke(prompt)
print(res.content)