class VanillaRAG:
    def __init__(self) -> None:
        """
        Initializes a new instance of the RAG class.
        """
        pass

    def vanilla_rag(self, query, chroma_collection, n_results=10):
        """
        Perform a vanilla RAG query.

        Parameters
        ----------
        query : str
            The query to be executed.
        chroma_collection : Chroma
            The Chroma collection to be queried.
        n_results : int, optional
            The number of results to be returned (default is 10).

        Returns
        -------
        rag_content : tuple of (dict, str)
            A tuple of (metadata, document) for each document in the query results.
        """
        results = chroma_collection.query(query_texts=[query], n_results=n_results)
        rag_content = tuple(zip(results["metadatas"][0], results["documents"][0]))
        return rag_content
