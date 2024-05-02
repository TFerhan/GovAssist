from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts.prompt import PromptTemplate
from pathlib import Path
from unidecode import unidecode
import tqdm
from langchain_community.vectorstores import FAISS
import accelerate

c_splitter = CharacterTextSplitter(
    
    chunk_size = 350,
    chunk_overlap = 4,
    separator = """,
      ]""",

)

def load_doc(file_path):
    loader = TextLoader(file_path)
    pages = loader.load()
    text_splitter = c_splitter
    doc_splits = text_splitter.split_documents(pages)
    return doc_splits



llm = HuggingFaceEndpoint(
            repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1',
            temperature = 0.17,
            max_new_tokens = 512,
            top_k = 30,
        )

def process_data():
  splt = load_doc('intents_v2.txt')
  embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
  db = FAISS.from_documents(splt, embeddings)
  return db

db = process_data()


prompt = """Vous êtes un formateur de modèles GPT. Vous excellez dans l'affinement des modèles GPT, la lecture et l'analyse de documents ainsi que l'association de balises aux entrées utilisateur appropriées.

Mon contexte consiste en un document structuré comportant des balises et leurs réponses associées respectivement, servant de référence pour former un modèle GPT capable de produire des réponses pertinentes en fonction des entrées utilisateur.

Votre tâche consiste à former un modèle GPT pour associer les entrées utilisateur aux balises adéquates et renvoyer les réponses correspondantes figurant dans le document de référence.

Les étapes à suivre sont les suivantes : analyser le document et ses balises, entraîner le modèle GPT avec les exemples fournis, mapper les entrées utilisateur aux balises correspondantes et générer les réponses associées.

Les caractéristiques du résultat attendu consistent en des réponses cohérentes et exactement adaptées aux balises fournies dans le document de référence.

Si tout va bien, allez-y.
        Human: {input}
        AI Assistant:
"""

        # Set up a conversational chain to retrieve and generate responses.
conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=db.as_retriever(),
            condense_question_prompt=PromptTemplate(input_variables=['input'], template=prompt),
        )

