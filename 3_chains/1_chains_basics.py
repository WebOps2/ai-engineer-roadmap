from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions about {club_name}."),
    ("user", "What year was {club_name} founded?"),
])


chain = prompt_template | llm | StrOutputParser() 


res = chain.invoke({"club_name": "Arsenal"})

print(res)