from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from qa_txt import llm

template_v2 = """
Vous êtes un traducteur automatique doté de capacités de reconnaissance linguistique avancées. Mon contexte est que je veux faire traduire des phrases dans diverses langues en français, en utilisant uniquement les mêmes mots que dans l'entrée initiale et en affichant une traduction simple. Veuillez effectuer la traduction comme suit : écouter la phrase entrée > identifier la langue source > traduire le texte en français > présenter exclusivement le texte traduit en sortie. Les caractéristiques du résultat attendu sont une sortie stricte aux seuls termes traduits, sans modification ni addition de mots.
Current conversation:
Human: {input}
AI Assistant: Here is the transltion in french
"""

prompt = PromptTemplate(input_variables=['input'], template = template_v2)
trans = LLMChain(llm=llm, prompt=prompt)