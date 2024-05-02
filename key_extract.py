from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from qa_txt import llm
# llm = HuggingFaceEndpoint(
#             repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1',
#             temperature = 0.2,
#             max_new_tokens = 10,
#             top_k = 30,
#             load_in_8bit = True,
#         )

template = """

        Vous êtes un Système d'Extraction de Mots-Clés personnalisé pour une utilisation dans un environnement WhatsApp Business. Son rôle consiste à reconnaître et isoler les mots-clés cruciaux contenus dans les demandes des utilisateurs. Il est impératif de garantir que la sortie comporte exactement un mot français, sans aucun contexte supplémentaire ni texte explicatif. Cette conformité aux directives permettra une compatibilité avec les fonctions subséquentes, telles que la recherche de sites Web contenant des sources de données publiques à l'aide du mot-clé fourni. De plus, veuillez extraire les mots-clés sous forme d'abréviations, tels que CNSS, MIC, ADD...
        Current conversation:
        Human: {input}
        AI Assistant:"""

prompt = PromptTemplate(input_variables=['input'], template = template)
chain = LLMChain(llm=llm, prompt=prompt)


