from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .retrieve_document import retrieve_document


llm = ChatOpenAI(model="gpt-4o-mini")
query = "Arsenal against Aston Villa in 2006-2007"

def generate_answer(query):
    documents = retrieve_document(query)

    context = "\n\n".join([doc.page_content for doc in documents])

    messages = [
        ("system", "You are a helpful assistant that can answer questions about the Premier League."),
        ("user", f"Context: {context}\n\nQuestion: {query}"),
    ]

    prompt_template = ChatPromptTemplate.from_messages(messages)

    prompt = prompt_template.invoke({"context": context, "query": query})

    res = llm.invoke(prompt)
    return res.content

if __name__ == "__main__":
    print(generate_answer(query))