from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions about {club_name}."),
    ("user", "What year was {club_name} founded?"),
])

translation_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a translator and convert the provided text into {language}."),
        ("human", "Translate the following text to {language}: {text}"),
    ]
)
prepare_for_translation = RunnableLambda(lambda x: {"text": x, "language": "spanish"})


# What does the lambda function do?
# It takes the output of the first chain and prepares it for the second chain.
# In this case, it takes the output of the first chain and adds the language to the input of the second chain.

chain = prompt_template | llm | StrOutputParser() | prepare_for_translation | translation_template | llm | StrOutputParser()

res = chain.invoke({"club_name": "Arsenal"})

print(res)