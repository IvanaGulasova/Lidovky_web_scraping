from requests import get
from bs4 import BeautifulSoup as bs
import csv

def main():
    adresa = "https://www.lidovky.cz/"
    web_url = get(adresa)
    soup = bs(web_url.text, features="html.parser")

    print(f"Sťahujem data zo zadanej url adresy: {adresa}")
    print("Prosím o trpezlivosť, chvíľu to potrvá.. \n")

    sekcie = vsetky_sekcie(soup)
    clanky = pocet_clankov(soup)
    vsetky_linky = linky(soup)
    vysledky = hlavne_vysledky(vsetky_linky)

    csv_sekcie = zapis_sekcii(sekcie)
    csv_clanky = hlavny_zapis(vysledky)
    csv_h3 = zapis_h3(clanky)

    print("Výsledky daných sekcií sú uložené v súbore --> sekcie.csv")
    print("Výsledky článkov sú uložené v súbore --> clanok_autor_datum.csv")
    print("Počet a názvy článkov na stránke sú uložené v súbore --> nadpisy_h3.csv \n")
    print("Ukončujem aplikáciu..")

def vsetky_sekcie(soup):
    tabulka_sekcie = soup.find("ul", {"class": "portalmenu-1 portalmenu-1b"})
    sekcie = tabulka_sekcie.find_all("a")
    nazvy_sekcii = [sekcia.text for sekcia in sekcie]

    zoznam_sekcii = []

    for poradie, sekcia in enumerate(nazvy_sekcii, 1):
        vysledok_sekcii = {
            "Poradie" : poradie,
            "Sekcia": sekcia
        }
        zoznam_sekcii.append(vysledok_sekcii)
    return zoznam_sekcii

def pocet_clankov(soup):
    finalny_zoznam = []
    zoznam_h3 = []
    cely_obsah = soup.find("div", {"id": "content"})
    nadpisy = cely_obsah.find_all("h3")

    for nadpis in nadpisy:
        zoznam_h3.append(nadpis.get_text())

    for poradie, nadpis in enumerate(zoznam_h3, 1):
        vysledky = {
            "Poradie": poradie,
            "Nadpis": nadpis
        }
        finalny_zoznam.append(vysledky)

    return finalny_zoznam

def linky(soup):
    linky_odkazy = []
    cely_obsah = soup.find("div", {"id": "content"})
    odkazy = cely_obsah.find_all("a", {"class": "art-link"})
    for odkaz in odkazy:
        href = odkaz.get("href")
        if href in linky_odkazy:
            continue
        elif "https://www.example.com" in href:
            continue
        linky_odkazy.append(href)

    return linky_odkazy

def hlavne_vysledky(linky_odkazy):
    zoznam_vysledkov = []

    for odkaz in linky_odkazy:
        nove_url = get(odkaz)
        soup2 = bs(nove_url.text, features="html.parser")

        try:
            hl_nadpis = soup2.find("h1", {"itemprop": "name headline"}).text
        except Exception:
            continue

        datum_clanku = soup2.find("span", {"itemprop": "datePublished"}).text
        if "NBSP" in datum_clanku:
            datum_clanku.replace("NBSP", " ")

        try:
            autor_clanku = soup2.find("span", {"itemprop": "name"}).text
        except AttributeError:
            autor_clanku = "Lidovky.cz"

        vysledok = {
            "Nadpis": hl_nadpis,
            "Autor": autor_clanku,
            "Datum": datum_clanku
        }

        zoznam_vysledkov.append(vysledok)
    return zoznam_vysledkov

def zapis_sekcii(zoznam_sekcii):
    with open("sekcie.csv", "w", newline="", encoding="utf-8") as file:
        hlava = zoznam_sekcii[0].keys()
        zapis = csv.DictWriter(file, fieldnames=hlava)
        zapis.writeheader()
        zapis.writerows(zoznam_sekcii)

def hlavny_zapis(zoznam_vysledkov):
    with open("clanok_autor_datum.csv", "w", newline="", encoding="utf-8") as file:
        hlava = zoznam_vysledkov[0].keys()
        zapis = csv.DictWriter(file, fieldnames=hlava)
        zapis.writeheader()
        zapis.writerows(zoznam_vysledkov)

def zapis_h3(clanky):
    with open("nadpisy_h3.csv", "w", newline="", encoding="utf-8") as file:
        hlava = clanky[0].keys()
        zapis = csv.DictWriter(file, fieldnames=hlava)
        zapis.writeheader()
        zapis.writerows(clanky)



if __name__ == "__main__":
    main()
