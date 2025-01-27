import os
import pymongo
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

def setup_model():
    # get local environment variables
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")

    # set up pinecone and open ai connections
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    retriever = vector_store.as_retriever(
            search_type='similarity',
            search_kwargs={'k': 3}
        )
    
    return retriever

def generate_response(user_input, retriever):

    # get local env vars for API call
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEV_PROMPT = os.getenv("DEV_PROMPT")

    # user_input = input("Enter your question: ")
    user_input = user_input
    res = retriever.invoke(user_input)

    rag_context = ', '.join([f"PLACE {i+1}: {place.page_content}" for i, place in enumerate(res)])

    llm = OpenAI(api_key=OPENAI_API_KEY)

    completion = llm.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'developer', 'content': DEV_PROMPT + rag_context},
            {'role': 'user', 'content': user_input}
        ]
    )

    return completion.choices[0].message


def connect_users():
    load_dotenv()

    DB_STRING = os.getenv("DB_STRING")
    DB = os.getenv("DATABASE")

    client = pymongo.MongoClient(DB_STRING)
    db = client[DB]

    return db
