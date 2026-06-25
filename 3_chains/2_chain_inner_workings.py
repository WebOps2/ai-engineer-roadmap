from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions about {club_name}."),
    ("user", "What year was {club_name} founded?"),
])

 
formal_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
invoke_model = RunnableLambda(lambda x: llm.invoke(x.to_messages()))
parse_output = RunnableLambda(lambda x: x.content)


chain = RunnableSequence(first=formal_prompt, middle=[invoke_model], last=parse_output)

res = chain.invoke({"club_name": "Arsenal"})

print(res)