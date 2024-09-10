from bs4 import BeautifulSoup
import pandas as pd
import pymupdf
import requests
from tqdm import tqdm

BASE_URL = 'https://papers.nips.cc/paper_files/paper/'

papers = []

for year in range(1987, 2024):
    print(f"---- PROCESSING YEAR {year} ----")

    # Get the list of papers for the given year
    response = requests.get(BASE_URL + str(year))

    # Convert to HTML soup and get list of paper links
    soup = BeautifulSoup(response.content, 'lxml')
    list_of_paper_links = soup.find_all('a', title='paper title')

    for a in tqdm(list_of_paper_links):
        paper = {}
        paper['year'] = year
        paper['name'] = a.string

        # Paper link format: BASE_URL/{year}/hash/{hash}-{suffix}.html
        paper_link_components = a.get('href').split('/')[-1].split('-')
        paper_hash = paper_link_components[0]
        paper_link_base_url = BASE_URL + str(year) + '/file/' + paper_hash

        if year >= 2020: # Raw paper text not available - process paper pdfs
            if year >= 2022: # URLS contain additional suffixes
                paper_suffix = paper_link_components[2].split('.')[0]
                pdf_url = paper_link_base_url + '-Paper-' + paper_suffix + '.pdf'
            else:
                pdf_url = paper_link_base_url + '-Paper.pdf'
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()
                # Stream response content into PDF doc
                pdf = pymupdf.Document(stream=response.content)
                # Convert PDF doc to raw text
                paper['text'] = chr(12).join([page.get_text() for page in pdf])
            except requests.exceptions.RequestException as e:
                print(f"Failed to download the PDF. Reason: {e}")
        else: # Raw paper text available via Metadata.json link
            metadata_url = paper_link_base_url + '-Metadata.json'
            try:
                response = requests.get(metadata_url)
                response.raise_for_status()
                # Extract raw paper text from paper metadata.json
                metadata_json = response.json()
                paper['text'] = metadata_json['full_text']
            except requests.exceptions.RequestException as e:
                print(f"Failed to download Metadata JSON. Reason: {e}")
                
        papers.append(paper)

df = pd.DataFrame(papers)
df.to_csv('papers.csv', index=False, header=True)
