#Importation des modules nécessaires

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#Définition des fonctions

def recuperer_texte_html(url):
    response = requests.get(url)
    texte_html = response.text
    return texte_html

def extraire_mots_cles(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    balise_meta = soup.find('meta', attrs={'name': 'keywords'})
    if balise_meta:
        mots_cles = balise_meta.get('content')
        mots_cles = mots_cles.split(',')[:3]
        mots_cles = [mot.strip() for mot in mots_cles]
        return mots_cles
    else:
        return []

def extraire_liens(url, texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    liens = soup.find_all('a')
    liens_entrants = []
    liens_sortants = []
    for lien in liens:
        href = lien.get('href')
        if href:
            parsed_href = urlparse(href)
            if parsed_href.netloc:
                liens_sortants.append(href)
            else:
                lien_complet = urlparse(url)._replace(path=parsed_href.path).geturl()
                liens_entrants.append(lien_complet)
    return liens_entrants, liens_sortants

def verifier_balises_alt(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    balises_img = soup.find_all('img')
    presence_alt = False
    for balise_img in balises_img:
        alt = balise_img.get('alt')
        if alt:
            presence_alt = True
            break
    return presence_alt

# Début du script

url = input("Entrez l'URL de la page à analyser : ")
texte_html = recuperer_texte_html(url)

mots_cles = extraire_mots_cles(texte_html)
print("Mots clés :")
for mot in mots_cles:
    print(mot)

liens_entrants, liens_sortants = extraire_liens(url, texte_html)
print("Nombre de liens entrants :", len(liens_entrants))
print("Nombre de liens sortants :", len(liens_sortants))

presence_balises_alt = verifier_balises_alt(texte_html)
if presence_balises_alt:
    print("Présence de balises alt : Oui")
else:
    print("Présence de balises alt : Non")
