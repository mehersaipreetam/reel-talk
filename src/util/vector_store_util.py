import hashlib

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from tqdm import tqdm
from config import logger


def _create_document(row):
    """
    Create a Document object from a pandas dataframe row.

    Parameters
    ----------
    row : pd.Series
        A pandas dataframe row containing the episode title, episode number,
        and content of the episode.

    Returns
    -------
    document : langchain_core.documents.Document
        A Document object containing the episode title and episode number as metadata
        and content of the episode as page content.
    """
    document = Document(
        page_content=row["content"],
        metadata={"episode": row["episode_num"], "title": row["title"]},
    )
    return document


def _generate_doc_id(document):
    """
    Generate a unique id for a document by hashing its content.

    Parameters
    ----------
    document : langchain_core.documents.Document
        A Document object containing the episode title and episode number as metadata
        and content of the episode as page content.

    Returns
    -------
    document : langchain_core.documents.Document
        A Document object with a unique id, containing the episode title and episode number as metadata
        and content of the episode as page content.
    """
    id = hashlib.md5(document.page_content.encode()).hexdigest()
    document.id = id
    return document


def add_to_vector_store(vector_store, df, max_tokens_per_chunk=384):
    """
    Add a pandas DataFrame to a vector store.

    The DataFrame should contain three columns. The first column should be named
    "title" and should contain the title of each episode. The second column
    should be named "episode_num" and should contain the episode number of each episode.
    The third column should be named "content" and should contain the content of each episode.

    Parameters
    ----------
    vector_store : langchain_core.vector_stores.VectorStore
        The vector store to which the episodes should be added.
    df : pd.DataFrame
        The pandas DataFrame containing the episodes to be added to the vector store.
    max_tokens_per_chunk : int
        The maximum number of tokens per chunk. The default value is 384 as sentence-transformers/all-mpnet-base-v2 supports only 384 tokens.

    Returns
    -------
    None
    """
    df["document"] = df.apply(_create_document, axis=1)
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=2048,
        chunk_overlap=128,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(df["document"])
    logger.info(f"Split {len(df["document"])} documents into {len(chunks)} chunks.")

    chunks = list(map(_generate_doc_id, chunks))
    batch_size = 100
    for i in tqdm(range(0, len(chunks), batch_size), desc="Adding to vector store"):
        vector_store.add_documents(chunks[i : i + batch_size])
    return
