# Documentation

Ce projet est un chatbot utilisant des Large Language Models génératifs, conçu pour le site `data.gov.ma` en tant que support de chat et pour aider à la recherche de données. Il est capable de comprendre toutes les langues, offrant ainsi une expérience utilisateur polyglotte.

Vous pouvez le testez directement [Testez ici](https://huggingface.co/spaces/tferhan/data_gov_ma).

https://github.com/TFerhan/GovAssist/assets/132760925/e02f0de6-f667-43c3-be7f-db784572ba36


Les fichiers dedans le dossier `chatbot` sont destinés à être hébergés sur `HuggingFace` pour un hébergement et une API gratuits. Déployer ces fichiers sur votre propre serveur nécessiterait environ 2,7 Go, ce qui est à la fois déconseillé et coûteux.

La solution préconisée consiste à héberger ces fichiers sur HuggingFace et à intégrer l'API fournie par `Gradio` sur votre serveur, puis dans le front-end pour les appels d'API.

Le dossier `front-end` contient les fichiers `.css`, `.html` et `.js` responsables de l'interface utilisateur.

Le dossier `api` contient le fichier `app.py` utilisé pour le déploiement de l'API Gradio. 

## Hiérarchie du Projet
-**chatbot**: Dossier contenant les fichiers nécessaire du model chatbot
  - **app.py**: Initialisation et déploiement de l'Agent.
  - **data_process.py**: Outils d'extraction et de nettoyage de données.
  - **intents_v2.txt**: Document contenant la documentation du site.
  - **key_extract.py**: Chaîne d'extraction des mots-clés depuis une requête.
  - **qa_txt.py**: Chaîne d'extraction de données depuis `intents_v2.txt`.
  - **requirements.txt**: Liste des dépendances Python pour l'application.
  - **trans.py**: Chaîne de traduction vers la langue française.
- **api**: Dossier de création de l'API.
  - **app.py**: Application Flask pour lancer l'API.
  - **requirements.txt**: Liste des dépendances Python pour l'application.
- **front-end**: Dossier front-end du chatbot.
  - **index.html**: Interface HTML.
  - **script.js**: Fichier JavaScript.
  - **style.css**: Fichier CSS.
  - **trbouch.png**: Image du chatbot.

## Fonctionnement

Utilisation du Framework `LangChain`, qui sert à développer des applications powered by Large Language Models. Elle est utilisée dans :
- **chatbot/app.py** : Pour la structuration des fonctions et l'initialisation de l'Agent.
- **key_extract.py** : L'initialisation de la chaîne avec une prompt spécifique pour l'extraction des mots-clés.
- **trans.py** : L'initiation d'une chaîne de traduction vers la langue française.
- **qa_txt** :
    - Vectorisation du document (intents_v2.txt) avec un sentence-transformer pour aider le modèle à trouver des réponses similaires (FAISS).
    - Création d'une chaîne de conversation qui prend en argument la requête de l'utilisateur et cherche dans le document une réponse fiable.

Utilisation du Framework BeautifulSoup pour le Web scraping, voir `data_process.py`.

Utilisation du modèle `Mixtral-8x7B-Instruct-v0.1`, un LLM génératif, car il est lightweight et disponible dans l'Inference API, et a une bonne accuracy supérieure à `OpenAI GPT-3.5`.

Utilisation du modèle `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` pour la vectorisation (embedding) des documents. Conçu pour la langue française.

Utilisation du VectorStore FAISS (Facebook AI Similarity Search) pour la recherche et l'extraction des données sous forme de vecteurs denses.

Utilisation du Framework `Gradio` car il offre une abstract API qui aide à offrir une belle interface du chatbot et aussi un hébergement gratuit.

Utilisation du Framework Flask pour la création d'une API avec une méthode POST qui retourne la réponse depuis l'API Gradio.

## Deploiement

Pour le déploiement, il est conseillé de déployer les fichiers dans le dossier `chatbot` sur `HuggingFace Spaces`. Pour ce faire, veuillez suivre ces étapes :

1. Créez un compte sur HuggingFace et accédez à Spaces.
2. Créez un Space et téléchargez les fichiers du dossier `chatbot`.
3. N'oubliez pas d'accéder aux paramètres du Space et d'ajouter votre access Token dans les sections des variables et secrets.

Cela permettra de déployer efficacement les fichiers du chatbot sur HuggingFace Spaces, offrant ainsi un hébergement et une accessibilité pratiques.
![image](https://github.com/TFerhan/GovAssist/assets/132760925/7d14e0fc-58ea-4611-8a62-1ec740741c29)

Une fois que l'application est en statut "Running", vous pouvez désormais accéder à l'API de Gradio en:
![image](https://github.com/TFerhan/GovAssist/assets/132760925/dd3e2ac8-f393-43aa-aa9a-f1a688f7e73f)

Vous pouvez désormais intégrer cette API dans votre application. Comme l'API en JavaScript n'est pas fonctionnelle, vous devrez créer une autre API en Flask qui utilise cette API Gradio afin de l'appeler dans l'interface JavaScript comme un lien POST
![image](https://github.com/TFerhan/GovAssist/assets/132760925/dd3f4a5f-33ab-4e8f-9a13-a7e3e8d5965d)

L'API Flask est située dans le fichier `api/app.py`. Dans ce fichier, une Thread est utilisée pour maintenir l'état "Running" du Space, car avec un hébergement gratuit, le Space passe en état "Sleeping" s'il n'est pas utilisé pendant 48 heures.

#### Documentation de l'API Flask

L'API Flask est conçue pour répondre à une requête POST avec un message au format JSON en argument. Elle retourne une chaîne de caractères en réponse.

- **Méthode HTTP** : POST

- **Endpoint** : `/api`

- **Arguments** :
  - `message` (JSON) : Le message à envoyer à l'API Gradio.

- **Réponse** :
  - Type : String
  - Description : La réponse de l'API Gradio.

#### Exemple d'utilisation :

```python
import requests

url = 'http://adresse_de_votre_api/api'
data = {'message': 'votre requete ici'}

response = requests.post(url, json=data)
print(response.text)
```


L'API Flask a été déployée sur Heroku pour permettre des tests dans l'interface. Vous avez également la possibilité de la déployer sur votre propre serveur. Son poids est de 28 Mo. Sur Heroku, son coût peut atteindre un maximum de 7 $ par mois.

Pour utiliser cette API, elle est appelée dans `front_end/script.js` à l'aide de la fonction fetch pour récupérer la réponse et rendre le chatbot dynamique.

## Notes
L'utilisation des modèles de HuggingFace est gratuite et peut être utilisée pour des projets commerciaux, car la plupart des modèles sont sous licence Apache 2.0. En revanche, les API populaires comme OpenAI nécessitent l'utilisation de tokens, ce qui peut être coûteux. Ce chatbot, s'il est hébergé sur votre propre serveur, peut ne rien vous coûter car il utilise des technologies open source.

Il convient également de noter que même si ce projet est conçu pour le site `data.gov.ma`, sa logique peut être adaptée à d'autres sites web. Cela en fait une bonne référence pour tout enthousiaste souhaitant héberger cette structure pour son propre service ou organisation.

Le problème du statut "Sleeping" peut également être résolu en améliorant le Space, bien que cela entraîne un coût minimal de 21 $ par mois. Cependant, l'utilisation d'un Thread a été testée et fonctionne bien.

Il est important de noter que ce projet nécessite davantage de tests avant le déploiement par des professionnels. Cela inclut la gestion des exceptions, la partie client-serveur, et d'autres aspects. Cependant, en ce qui concerne le développement du modèle conversationnel, même s'il n'est pas parfait, il fait un bon travail par rapport aux autres chatbots qui se basent sur la classification des entrées.



Enfin, ce projet a été réalisé dans le cadre d'un stage émis par l'ADD ( Agence de développement du Digital). Si vous souhaitez en savoir plus sur mon parcours ou me contacter, vous pouvez consulter mon profil LinkedIn :

- **Ferhan Taha**
  - LinkedIn: [Ferhan Taha on LinkedIn](https://www.linkedin.com/in/tferhan/)
  - Email: taha.ferhan@hotmail.com
