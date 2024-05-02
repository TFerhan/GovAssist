import re
from bs4 import BeautifulSoup
import requests

def nettoyer_string(mot):
  mot_non_special = re.sub(r'[^\w\sÀ-ÿ]' , '', mot)
  mot_ns_ne = re.sub(r'\s+', ' ', mot_non_special)
  mot_final = mot_ns_ne.strip()


  return mot_final


def chercher_data(mot,titles = [], links = [] ): #Scraping data links from the website
    response = requests.get("https://data.gov.ma/data/fr/dataset",  params={'q': mot})
    if response.status_code != 200:
        return titles, links, response.url, 0
    soup = BeautifulSoup(response.text, features="lxml")
    nb_text = soup.find('h1').text
    nombre_don = re.findall(r'\d+', nb_text)
    media = soup.find('ul', class_='dataset-list list-unstyled')
    if media:
      thm = media.find_all('li', class_ = 'dataset-item')
      for m in thm:
            link = m.find('a')['href']
            links.append('https://data.gov.ma' + link)
            title = m.find('h2').text.strip()
            titles.append(title)
    else:
      return titles, links,  response.url, 0

    if not titles:
      return titles, links, response.url, 0

    return titles, links ,response.url, nombre_don[0]


def format_reponse(data): #structuring the scrapped data
    if len(data[0]) == 1:
          response = f"Ici le lien vers la donnée correspondant au mot recherché : {data[-2]}\n"
          response += f"Voici le seul résultat trouvé :\n"
          response += f"Titre : {data[0][0]}\n"
          response += f"Lien : {data[1][0]}\n"
          return response
    else:
          response = f"Ici le lien vers toutes les {data[-1]} données correspondant au mot recherché : {data[-2]}\n"
          response += f"Voici un exemple parmi les résultats trouvés :\n"
          response += f"Titre : {data[0][-1]}\n"
          response += f"Lien : {data[1][-1]}\n"
          return response
