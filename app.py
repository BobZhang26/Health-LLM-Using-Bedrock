# Sys and basics
import json, os, sys, boto3
import streamlit as st
from botocore.exceptions import ClientError

# Embeddings
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

# Data ingestion
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Vector Embedding and Store
from langchain_community.vectorstores import FAISS

# LLM Models
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from dotenv import load_dotenv
from PIL import Image


def get_secret(secret_key):

    secret_name = "aws_creds"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Parse the SecretString into a dictionary
    secret_dict = json.loads(get_secret_value_response["SecretString"])

    # Get the value of the secret key from the dictionary
    secret_value = secret_dict.get(secret_key)

    return secret_value


# Set the AWS credentials as environment variables
os.environ["key_id"] = get_secret("AWS_ACCESS_KEY_ID")
os.environ["secret_key"] = get_secret("AWS_SECRET_ACCESS_KEY")
os.environ["def_region"] = get_secret("AWS_DEFAULT_REGION")

load_dotenv()
session = boto3.Session(
    aws_access_key_id=os.getenv("key_id"),
    aws_secret_access_key=os.getenv("secret_key"),
    region_name=os.getenv("def_region"),
)

bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1", client=bedrock
)


# Data Ingestion
def data_ingestion():
    # Data ingestion
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()

    # Splitting the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    docs = text_splitter.split_documents(documents)
    return docs


# Vector Embedding and Store
def get_vector_store(docs):
    vectorstore_faiss = FAISS.from_documents(docs, bedrock_embeddings)
    vectorstore_faiss.save_local("faiss_index")


def get_titan_exp():
    # Create anthropic model
    llm = Bedrock(
        model_id="amazon.titan-text-express-v1",
        client=bedrock,
    )
    return llm


prompt_template = """
Human: Based on the context, provide a detailed answer (min. 250 words) to the question. If unsure, admit it.
<context>
{context}
</context>

Question: {question}

Assistant:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def get_response_llm(llm, vectorstore_faiss, query):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore_faiss.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )
    answer = qa({"query": query})
    return answer["result"]


def main():
    st.set_page_config(
        page_title="Health Encyclopedia",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    image = Image.open("What-is-digital-health-technology.jpg.jpg")
    st.image(image, width=500)  # Set the width to the desired value

    st.title("Welcome to the Health Encyclopedia")
    st.markdown(
        """
        Welcome to the Health Encyclopedia. Here you can ask questions about health and get detailed answers from our extensive database of health-related documents.
        """
    )

    user_question = st.text_input("Ask Questions to our Health Encyclopedia:")

    with st.sidebar:
        st.title("Update Or Create Vector Store:")

        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Done")

    if st.button("Search"):
        with st.spinner("Searching..."):
            faiss_index = FAISS.load_local(
                "faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True
            )
            llm = get_titan_exp()
            st.write(get_response_llm(llm, faiss_index, user_question))
            st.success("Done")


if __name__ == "__main__":
    main()
