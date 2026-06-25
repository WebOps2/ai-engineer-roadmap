from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableParallel
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-nano",
)

summary_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a movie critic."),
        ("human", "Provide a brief summary of the movie {movie_name}."),
    ]
)

def analyze_plot(plot):
    plot_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a movie critic."),
            ("human", "Analyze the plot of the movie {plot}."),
        ]
    )
    return plot_template.format_prompt(plot=plot)

def analyze_characters(characters):
    characters_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a movie critic."),
            ("human", "Analyze the characters of the movie {characters}."),
        ]
    )
    return characters_template.format_prompt(characters=characters)


def combine_verdicts(plot_analysis: str, characters_analysis: str) -> str:
    return  f"Plot Analysis:\n{plot_analysis}\n\nCharacter Analysis:\n{characters_analysis}"

plot_branch_chain = (
    RunnableLambda(lambda x: analyze_plot(x)) | llm | StrOutputParser()
)

characters_branch_chain = (
    RunnableLambda(lambda x: analyze_characters(x)) | llm | StrOutputParser()
)

chain = (
    summary_template | llm | StrOutputParser() 
    | RunnableParallel(branches={"plot": plot_branch_chain, "characters": characters_branch_chain}) 
    | RunnableLambda(lambda x: combine_verdicts(x["branches"]["plot"], x["branches"]["characters"]))
)

res = chain.invoke({"movie_name": "The Dark Knight"})
print(res)