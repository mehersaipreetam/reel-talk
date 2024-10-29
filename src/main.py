import argparse

import chromadb
import dotenv

from prompts import VanillaRAGPrompt
from src.llm import LLM
from src.rag.vanilla_rag import VanillaRAG
from src.util.data_util import save_content_to_path
from src.util.parser_util import get_all_episodes_df
from src.vector_store.chromadb import ChromaDB

if __name__ == "__main__":
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create_db",
        dest="create_db",
        type=bool,
        help="Flag to create DB",
        default=False,
    )
    parser.add_argument(
        "--csv_path",
        dest="csv_path",
        type=str,
        help="Path of csv file with scraped data",
        default="../data/how_i_met_your_mother.csv",
    )
    parser.add_argument(
        "--db_path",
        dest="db_path",
        type=str,
        help="Path of the chroma db",
        default="../data/chroma_langchain_db",
    )
    parser.add_argument(
        "--collection_name",
        dest="collection_name",
        type=str,
        help="Name of the chroma collection",
        default="how_i_met_your_mother",
    )
    parser.add_argument("--query", dest="query", type=str, help="Query to be answered")

    args = parser.parse_args()

    if args.create_db:
        url_fandom = "https://how-i-met-your-mother.fandom.com/wiki/Episode_Guide"
        episode_df = get_all_episodes_df(url_fandom)
        save_content_to_path(episode_df, args.csv_path)

        chromadb_store = ChromaDB(
            collection_name=args.collection_name,
            embedding_function_name="sentence-transformers/all-MiniLM-L6-v2",
            persist_directory=args.db_path,
        )
        chromadb_store.add_episode_df_to_vector_store(episode_df)

    client = chromadb.PersistentClient(path=args.db_path)
    chroma_collection = client.get_or_create_collection(name=args.collection_name)

    vanilla_rag = VanillaRAG()
    retrieved_documents = vanilla_rag.vanilla_rag(
        query=args.query, chroma_collection=chroma_collection, n_results=10
    )

    prompt = VanillaRAGPrompt.format(
        query=args.query, retrieved_documents=retrieved_documents
    )
    llm = LLM()
    response = llm.invoke_llm(prompt)
    print("\n\n\n***** Response *****")
    print(response.content)
    print("\n\n\n")
