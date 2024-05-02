from langchain.prompts import StringPromptTemplate
import re
import langchain
from qa_txt import conversation_chain
from key_extract import chain
from bs4 import BeautifulSoup
import requests
from data_process import *
from langchain.tools.base import StructuredTool
from langchain.agents import initialize_agent
from qa_txt import llm
from trans import trans
import gradio as gr
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
    tool,
)
from langchain import hub



prompt = hub.pull("hwchase17/react") #A prompt to structure the message for the agent

def faq(query: str) -> str: #For Q&A from the document intents_v2
    reponse = conversation_chain.invoke({"question": query, "chat_history": []}) #chain in qa_txt.py file
    return reponse['answer']

qa_faq = StructuredTool.from_function(
    func = faq ,
    description="""
    Respond to general questions about the website like the documentation, contact, utility, support... Don't use it when the user request data about a subject (economie, justice, water, or any type of public dataset) only for contact or useful links data.

    Parameters :
    - query (string) : the same input as the user input no more no less and dont translate it even if it is in another language.

    Returns :
    - string : the output as returned from the function in french.
    """
)

def request_data(query: str) -> str: #For extracting data from the website 
    request = chain.invoke({"input": query})['text'] #This chain extract the keyword based on the context
    mot_cle = nettoyer_string(request)
    mots = mot_cle.split()
    ui = mots[0]
    rg = chercher_data(ui) #This function scrap data based on the keyword extracted can be found in data_process.py
    if len(rg[0]):
      reponse_final = format_reponse(rg)
      return reponse_final
    else:
      return "Désolé, il semble que nous n'ayons pas de données correspondant à votre demande pour le moment. Avez-vous une autre question ou avez-vous besoin d'aide sur quelque chose d'autre?"

fetch_data = StructuredTool.from_function(
    func=request_data,
    description="""
    Request and fetch data using a search keyword.

    Parameters :
    - query (string) : the same input as the user input no more no less and always it must be in french if it isn't already. For example : "give me data about health" the input is health in french which is santé, same for other languages and the words translatted must be nouns not adjectives or verbs also the user may request data about an organization where you need to take just the main subject for example "Je veux les données de l'agence de développement digitale" you take just "développement".
    Returns :
    - string : the output as returned from the function in french , includes the link to all the data about the keyword along with an example.
    """,
)

def translate(query: str) -> str: #For translation in french because the website operates in french language
    translated = trans.invoke({"input": query})['text']
    return translated

translate_text = StructuredTool.from_function(
    func=translate,
    description= """
    Translate from any language to french. Don't use it if the text is already in french

    Parameters :
    - query (string) : the same input as the user input no more no less.
    Returns :
    - string : isolate just the translated text in french with no other useless words.
    """,
)

tools_add = [ #List of tools above
    qa_faq,
    fetch_data,
    translate_text,
]

agent = create_react_agent(llm=llm, tools=tools_add, prompt=prompt) #llm is imported from qa_txt.py

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools_add,
    verbose=True, #To provide more words
    max_iterations = 10, #To not lose the agent in a infinite loop if he doesn't understand the query
    #max_execution_time = 45, optional but useful for timeout
    
)

def data_gov_ma(message, history):
  try:
    response = agent_executor.invoke({"input": message}) #running the agent
    final_response = response['output']
    timeout_iteration_error = 'Agent stopped due to iteration limit or time limit.' #Exception error due to max iterations or timeout
    if final_response == timeout_iteration_error:
        return "Je suis désolé, je n'ai pas compris votre question.Pourriez-vous la reformuler s'il vous plaît ?"
    else:
        return final_response
  except ValueError as e: #For any other Exception
    return "Je suis désolé, je n'ai pas compris votre question.Pourriez-vous la reformuler s'il vous plaît ?"

gr.ChatInterface(data_gov_ma).launch() #lunching gradio api
