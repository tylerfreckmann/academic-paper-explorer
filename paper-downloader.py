from bs4 import BeautifulSoup
import os
import requests
from tqdm import tqdm

BASE_URL = 'https://papers.nips.cc/paper_files/paper/'

for year in range(1987, 2024):
    print(f'---- PROCESSING YEAR {year} ----')

    year_directory = f'papers/{year}'
    if not os.path.exists(year_directory):
        os.makedirs(year_directory)

    # Get the list of papers for the given year
    response = requests.get(BASE_URL + str(year))
    soup = BeautifulSoup(response.content, 'lxml')
    list_of_paper_links = soup.find_all('a', title='paper title')

    # For each paper link
    for a in tqdm(list_of_paper_links):
        # Paper link format: BASE_URL/{year}/hash/{hash}-{suffix}.html
        paper_link_components = a.get('href').split('/')[-1].split('-')
        paper_hash = paper_link_components[0]
        paper_link_base_url = BASE_URL + str(year) + '/file/' + paper_hash
        
        # Get PDF URL
        if year >= 2022: # URLS contain additional suffixes
            paper_suffix = paper_link_components[2].split('.')[0]
            pdf_url = paper_link_base_url + '-Paper-' + paper_suffix + '.pdf'
            pdf_filename = paper_hash + '-Paper-' + paper_suffix + '.pdf'
        else:
            pdf_url = paper_link_base_url + '-Paper.pdf'
            pdf_filename = paper_hash + '-Paper.pdf'
        
        # Check if paper already downloaded
        pdf_path = os.path.join(year_directory, pdf_filename)
        if not os.path.exists(pdf_path):
            # Download paper
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download the PDF. Reason: {e}")
