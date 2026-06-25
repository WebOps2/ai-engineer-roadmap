from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

positive_response_passing_grade_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful high school teacher."),
        ("human", "Generate a positive response from the parent based on their child's grades. {grades}."),
    ]
) 

negative_response_passing_grade_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful high school teacher."),
        ("human", "Generate a negative response from the parent based on their child's grades. {grades}."),
    ]
)

classification_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful high school teacher."),
        ("human", "Classify the following response into a pass or fail. If the grades {grades} are greater than or equal to 70, return 'pass'. If the grades {grades} are less than 70, return 'fail'."),
    ]
)

branches = RunnableBranch(
    (
        lambda x: "pass" in x.lower(),
        positive_response_passing_grade_template | llm | StrOutputParser()
    ),
    (
        lambda x: "fail" in x.lower(),
        negative_response_passing_grade_template | llm | StrOutputParser(),
    ),
    positive_response_passing_grade_template | llm | StrOutputParser(),
)

classification_chain = classification_template | llm | StrOutputParser() 



chain = classification_chain | branches

res = chain.invoke({"grades": "45"})

print(res)