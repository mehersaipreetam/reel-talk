from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.util.vector_store_util import add_to_vector_store


class ChromaDB:
    def __init__(self, collection_name, embedding_function_name="sentence-transformers/all-MiniLM-L6-v2", persist_directory="../data/chroma_langchain_db"):
        """
        Parameters
        ----------
        collection_name : str
            The name of the collection of vectors that will be stored in the vector
            store.
        embedding_function_name : str
            The name of the Hugging Face model that will be used to generate the
            embedding vectors.
        persist_directory : str
            The directory where the vector store data will be persisted.

        Attributes
        ----------
        embeddings : HuggingFaceEmbeddings
            The Hugging Face embeddings object that will be used to generate the
            embedding vectors.
        vector_store : Chroma
            The Chroma vector store object that will be used to store the
            embedding vectors.
        """
        embeddings = HuggingFaceEmbeddings(model_name=embedding_function_name)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
    
    def add_episode_df_to_vector_store(self, episode_df):
        """
        Add a pandas DataFrame to the vector store.

        The DataFrame should contain two columns. The first column should be named
        "title" and should contain the title of each episode. The second column
        should be named "content" and should contain the content of each episode.

        Parameters
        ----------
        episode_df : pd.DataFrame
            The pandas DataFrame containing the episodes to be added to the
            vector store.

        Returns
        -------
        None
        """
        add_to_vector_store(self.vector_store, episode_df)
        return
