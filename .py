import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def kopyala(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')


        title = soup.title.string if soup.title else 'No Title'
        folder_name = title.replace(" ", "_")
        os.makedirs(folder_name, exist_ok=True)

        with open(os.path.join(folder_name, f"{folder_name}.html"), "w", encoding="utf-8") as file:
            file.write(html_content)

        kaynakları_indir(soup, url, folder_name)

        print(f"{folder_name} klasörü oluşturuldu ve içerik kaydedildi.")

    except requests.exceptions.RequestException as e:
        print(f"Bir hata oluştu: {e}")

def kaynakları_indir(soup, base_url, folder_name):
    for link in soup.find_all(['link', 'script', 'img']):
        if link.name == 'link' and 'href' in link.attrs:
            resource_url = urljoin(base_url, link['href'])
            download_resource(resource_url, folder_name)

        elif link.name == 'script' and 'src' in link.attrs:
            resource_url = urljoin(base_url, link['src'])
            download_resource(resource_url, folder_name)

        elif link.name == 'img' and 'src' in link.attrs:
            resource_url = urljoin(base_url, link['src'])
            download_resource(resource_url, folder_name)

def download_resource(url, folder_name):
    try:
        response = requests.get(url)
        response.raise_for_status()

        filename = os.path.join(folder_name, os.path.basename(url))
        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"{filename} indirildi.")

    except requests.exceptions.RequestException as e:
        print(f"Kaynak indirilemedi: {e}")

if __name__ == "__main__":
    url = input("Kopyalamak istediğiniz URL'yi girin: ")
    kopyala(url)
