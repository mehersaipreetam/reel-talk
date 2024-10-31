# Reel Talk

Reel Talk is an interactive application designed for the fans of the show *How I Met Your Mother* (HIMYM). This app uses RAG techniques to deliver meaningful, contextually aware answers to your questions about the show. 

## Prerequisites

Before you start, make sure you have the following set up:

### 3. Populate the `.env` File
Create a `.env` file in the project root directory with the following variables:

```plaintext
GROQ_API_KEY=your_groq_api_key
```

## Installation and Setup

### 1. Create a Conda Environment
To isolate dependencies, create and activate a Conda environment:
conda create -n reel-talk python=3.12.5
conda activate reel-talk

### 2. Install the Required Packages
Navigate to the main directory and install the required Python packages:
```bash
pip install -e .
```

### 3. Run the Streamlit App
Navigate to the src directory and launch the web application using Streamlit:
```bash
cd src
streamlit run streamlit.py
```

## Future Steps

To further improve the user experience and the app's ability to handle more complex queries, future updates will aim to:

- **Enhance RAG Capabilities**: Implement more advanced RAG techniques.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://docs.trychroma.com/)
- [Groq](https://groq.com/)
- [HIMYM Fandom](https://how-i-met-your-mother.fandom.com/wiki/How_I_Met_Your_Mother_Wiki)

## Contact
If you have any questions or suggestions, feel free to reach out. You can contact me at mehersaipreetam@gmail.com. I’ll be happy to assist!
