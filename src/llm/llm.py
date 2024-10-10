import logging
from langchain_groq import ChatGroq

from config import logger

class LLM:
    def __init__(self) -> None:
        self.llm = self.get_llm()
    
    def get_llm(self, model="llama3-70b-8192"):
        """
        Initializes and returns an instance of the ChatGroq LLM with specified configurations. Support for other LLMs can be added as well

        Parameters
        ----------
        model : str, optional
            The name of the language model to be used (default is "llama3-70b-8192").

        Returns
        -------
        ChatGroq
            An instance of the ChatGroq LLM configured with the specified parameters.
        """
        llm = ChatGroq(
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        return llm

    def invoke_llm(self, prompt):
        """
        Invokes the given language model with the given prompt, and returns the model's response.

        Parameters
        ----------
        prompt : str
            The string prompt to be passed to the language model.

        Returns
        -------
        str
            The output of the language model.
        """
        logger.info(f"Invoking LLM with prompt: {prompt}")
        response = self.llm.invoke(prompt)
        logger.info(f"LLM response: {response}")
        return response