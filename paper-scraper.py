from bs4 import BeautifulSoup
import os
import requests
import shutil

YEARS = [str(year) for year in range(2023, 2024)]
BASE_URL = 'https://papers.nips.cc/paper_files/paper/'
PAPER_PDF_DIRECTORY = 'paper_pdfs'

if os.path.exists(PAPER_PDF_DIRECTORY):
    shutil.rmtree(PAPER_PDF_DIRECTORY)

os.makedirs(PAPER_PDF_DIRECTORY)

for year in YEARS:
    os.makedirs(PAPER_PDF_DIRECTORY + '/' + year)
    response = requests.get(BASE_URL + year)
    soup = BeautifulSoup(response.content, 'lxml')
    # Paper link format: BASE_URL/{year}/hash/{hash}-Abstract-Conference.html
    paper_hashes = [li.a.get('href').split('/')[-1].split('-')[0] for li in soup.select('.paper-list > li')]
    for hash in paper_hashes:
        pdf_file_name = hash + '-Paper-Conference.pdf'
        file_path = PAPER_PDF_DIRECTORY + '/' + year + '/' + pdf_file_name
        pdf_url = BASE_URL + year + '/file/' + pdf_file_name
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF downloaded and saved to '{file_path}'.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the PDF. Reason: {e}")
