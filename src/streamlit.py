import base64
import streamlit as st
from PIL import Image
import streamlit as st
import dotenv
from prompts import VanillaRAGPrompt
from src.llm import LLM
from src.rag.vanilla_rag import VanillaRAG
import chromadb

# background_image = Image.open("himym.jpg")

st.set_page_config(layout="wide", page_title="Reel Talk - HIMYM Theme")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64_of_bin_file("himym.jpg")
page_bg_css = f"""
<style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    .main-content {{
        background-color: rgba(0, 0, 0, 0.7);  /* Darker semi-transparent background */
        padding: 20px;
        border-radius: 10px;
        width: 100%;
    }}
    h1, h2, h3, h4, h5, h6, p {{
        color: white;  /* Ensure text is bright */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);  /* Add shadow for better contrast */
    }}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)

st.title("Reel Talk - How I Met Your Mother Edition")
st.subheader("Got a question about the legen—wait for it—dary show 'How I Met Your Mother'? Ask away!")

dotenv.load_dotenv()

query = st.text_input("What's your question?", value="", placeholder="Ask me anything about HIMYM!")
chroma_db_path = "../data/chroma_langchain_db"
collection_name = "how_i_met_your_mother"

if st.button("Submit"):
    if query:
        client = chromadb.PersistentClient(path=chroma_db_path)
        chroma_collection = client.get_or_create_collection(name=collection_name)
        
        # Initialize VanillaRAG and retrieve documents
        vanilla_rag = VanillaRAG()
        retrieved_documents = vanilla_rag.vanilla_rag(
            query=query, chroma_collection=chroma_collection, n_results=10
        )
        
        # Format the prompt and get response from LLM
        prompt = VanillaRAGPrompt.format(query=query, retrieved_documents=retrieved_documents)
        llm = LLM()
        response = llm.invoke_llm(prompt)
        st.markdown("### Response:")
        st.write(response.content)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.write("Didn't quite catch that, bro! Give it another shot!")
