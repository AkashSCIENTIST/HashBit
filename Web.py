import streamlit as st
import csv
import os
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import Document
from dotenv import load_dotenv
load_dotenv()


def read_csv_into_vector_document(file, text_cols):
    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        text_data = []
        for row in csv_reader:
            text = ' '.join([row[col] for col in text_cols])
            text_data.append(text)
        return [Document(page_content=text) for text in text_data]


# Define the layout using neomorphic design
st.set_page_config(
    page_title="Neomorphic Website",
    page_icon=":clipboard:",
    layout="wide"
)

st.markdown(
    """
    <style>
    .neumorphic {
        padding: 15px;
        background: #272829;
        border-radius: 14px;
        row-gap : 6px;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Top panel
st.title("PSGCT INCIDENT RESOLVER")


api_key = os.environ.get("OPEN_API_KEY")
key_status = True
if not api_key:
    print('OpenAI API key not found in environment variables.')
    key_status = False

data = read_csv_into_vector_document("newdata.csv", ["type", "issue", "resolution", "description"])
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectors = FAISS.from_documents(data, embeddings)
chain = ConversationalRetrievalChain.from_llm(
    llm = ChatOpenAI(
        temperature=0.0, 
        model_name='gpt-3.5-turbo', 
        openai_api_key=api_key
        ), 
    retriever=vectors.as_retriever())
history = []

if key_status:
    with st.form(key="suggestion_form"):
        suggestion = st.text_input("Enter your Incident:", key="input_suggestion")
        submitted = st.form_submit_button("Submit")
        submit_code = """
        <script>
        document.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                document.querySelector(".stButton button").click();
                event.preventDefault();
            }
        });
        </script>
        """
        st.markdown(submit_code, unsafe_allow_html=True)
        if submitted:
            if suggestion:
                st.success("Incident submitted! Waiting for resolution ...")

                query = suggestion
                with st.spinner(text="Incident submitted! Waiting for resolution ..."):
                    res = chain({"question": query, "chat_history": history})
                
                print(res["answer"])
                history.append((query, res["answer"]))

                for data in history[::-1]:
                    q = data[0]
                    res = data[1]
                    container = st.container()
                    container.code("Incident\n" + q + "\nResolution:\n" + res)
                    container.divider()
else:
    st.header("Key not found in .env")
