import streamlit as st
import boto3
import sys, json, os
from streamlit_extras.add_vertical_space import add_vertical_space
from ingest import ingest_and_confirm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib_helpers.pdf_helpers import upload_pdf_from_streamlit
import time

# from streamlit_chat import message
# import random
# import string

region = boto3.Session().region_name
# region = "us-west-2"
region = "us-east-1"
session = boto3.Session(region_name=region)
lambda_client = session.client("lambda")
# print(lambda_client)
knowledge_base_id = "RL7V0ZUTI6"
data_source_id = "ADIAXAKE25"

st.set_page_config(
    page_title="Improving-Medical-Guidelines-for-Duke-Health-with-RAG-LLMs",
    page_icon=":robot:",
)

with st.sidebar:
    st.title("🤗💬 DukeHealth AI App")

    # Add file upload button to the sidebar
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        file_path = "../pdfs/" + uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call the upload_pdf_from_streamlit function
        upload_pdf_from_streamlit(file_path)
        st.text("Uploaded file to pdfs directory")

        time.sleep(5)
        ingest_and_confirm(knowledge_base_id, data_source_id)
        st.success("Document Successfully added to Knowledge Base")

    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using the RAG architecture. It is designed to provide information on medical guidelines for Duke Health.
                
    Contributors:
    1. Bob Zhang
    2. Osama Ahmed
    3. Doyinsolami Olaoye
    4. Eric Rios
    5. Suim Park
    """
    )
    add_vertical_space(5)
    st.write("Made with ❤️ by Duke BODES Team")


# st.title("Test Chatbot using Knowledge Bases for Amazon Bedrock")

sessionId = ""
# sessionId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
# print(sessionId)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session id
if "sessionId" not in st.session_state:
    st.session_state["sessionId"] = sessionId

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me a question here..."):

    # Display user input in chat message container
    question = prompt
    st.chat_message("user").markdown(question)

    # Call lambda function to get response from the model
    payload = json.dumps(
        {"question": prompt, "sessionId": st.session_state["sessionId"]}
    )
    print(payload)
    result = lambda_client.invoke(FunctionName="InvokeKnowledgeBase", Payload=payload)
    # print(result)
    result = json.loads(result["Payload"].read().decode("utf-8"))
    print(result)

    answer = result["body"]["answer"]
    references = result["body"]["references"]
    sessionId = result["body"]["sessionId"]

    st.session_state["sessionId"] = sessionId

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(answer)
        # if references:
        #     st.markdown("References: "+ references[0]['location']['s3Location']['uri'][40:])
        if references:
            st.write("📚 **References:**")
            out_ref = set()
            for i in range(len(references)):
                # references[0]['location']['s3Location']['uri'][40:])
                if references[i]["location"]["s3Location"]["uri"] in out_ref:
                    continue
                out_ref.add(references[i]["location"]["s3Location"]["uri"])
                reference = references[i]["location"]["s3Location"]["uri"][40:].replace(
                    ".pdf", ""
                )
                st.write(
                    f"{i+1}. {references[i]['location']['s3Location']['uri'][40:]}"
                )

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})


# add readme file to github repo
# edit user interface
# stop using
# list references
# update knowledge base
