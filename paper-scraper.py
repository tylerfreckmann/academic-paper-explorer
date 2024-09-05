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
    paper_list = [li.a for li in soup.select('.paper-list > li')]
    for a in paper_list[:10]:
        paper_name = a.string
        paper_link_components = a.get('href').split('/')[-1].split('-')
        paper_hash = paper_link_components[0]
        paper_suffix = paper_link_components[2].split('.')[0]
        file_path = PAPER_PDF_DIRECTORY + '/' + year + '/' + paper_name + '.pdf'
        pdf_url = BASE_URL + year + '/file/' + paper_hash + '-Paper-' + paper_suffix + '.pdf'
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF downloaded and saved to '{file_path}'.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the PDF. Reason: {e}")
