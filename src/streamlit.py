import base64
import streamlit as st
from PIL import Image
import streamlit as st
import dotenv
from prompts import VanillaRAGPrompt
from src.llm import LLM
from src.rag.vanilla_rag import VanillaRAG
import chromadb

from util.data_util import save_content_to_path
from util.parser_util import get_all_episodes_df
from vector_store.chromadb import ChromaDB

st.set_page_config(layout="wide", page_title="Reel Talk - HIMYM Theme")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64_of_bin_file("himym.jpg")
page_bg_css = f"""
<style>
    .stApp {{
        background: rgba(0, 0, 0, 0.1) url("data:image/jpeg;base64,{bin_str}") no-repeat center center fixed; 
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    .main-content {{
        background-color: rgba(0, 0, 0, 0.3);  /* Darker semi-transparent background */
        padding: 20px;
        border-radius: 10px;
        width: 100%;
    }}
    h1, h2, h3, h4, h5, h6, p {{
        color: white;  /* Ensure text is bright */
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.8);  /* Add shadow for better contrast */
    }}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)

st.title("Reel Talk - How I Met Your Mother Edition")
st.subheader("Got a question about the legen—wait for it—dary show 'How I Met Your Mother'? Ask away!")

dotenv.load_dotenv()

check_placeholder = st.empty()
data_available = check_placeholder.selectbox("Do you have data available?", ["", "Yes", "No"])

message_placeholder = st.empty()

if data_available == "No":
    message_placeholder.write("Let's create some data first! Please wait")
    url_fandom = "https://how-i-met-your-mother.fandom.com/wiki/Episode_Guide"
    episode_df = get_all_episodes_df(url_fandom)

    csv_path = "../data/how_i_met_your_mother.csv"
    save_content_to_path(episode_df, csv_path)
    
    collection_name = "how_i_met_your_mother"
    db_path = "../data/chroma_langchain_db"
    chromadb_store = ChromaDB(
        collection_name=collection_name,
        embedding_function_name="sentence-transformers/all-MiniLM-L6-v2",
        persist_directory=db_path,
    )
    chromadb_store.add_episode_df_to_vector_store(episode_df)
    st.success("Data has been created and stored successfully!")
    message_placeholder.empty()
    data_available = "Yes"
 
if data_available == "Yes":
    check_placeholder.selectbox("Do you have data available?", ["Yes", "No"]) 
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
