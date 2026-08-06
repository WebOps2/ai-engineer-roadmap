from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .retrieve_document import retrieve_document


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
query = "Arsenal against Aston Villa in 2006-2007"

def generate_answer(query):
    documents = retrieve_document(query)
    if not documents:
        return "No results found in the dataset."

    context = "\n\n".join([doc.page_content for doc in documents])

    prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You answer questions using only the supplied dataset context.
        Rules:
        - Do not use outside knowledge.
        - Do not invent or assume missing information.
        - If the context does not explicitly answer the question,
          respond with exactly: NO_RESULTS
        Context:
        {context}
        """,
    ),
    ("human", "{query}"),
])

    prompt = prompt_template.invoke({"context": context, "query": query})

    res = llm.invoke(prompt)
    answer = str(res.content).strip()
    if answer == "NO_RESULTS":
        return "No results found in the dataset."
    return answer

if __name__ == "__main__":
    print(generate_answer(query))