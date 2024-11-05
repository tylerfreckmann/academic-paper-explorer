import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

BASE_URL = 'https://papers.nips.cc/paper_files/paper/'
MAX_RETRIES = 3
NUM_WORKERS = 40  # Number of concurrent threads for downloading papers

# Set up logging
logging.basicConfig(
    filename='paper_download.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_paper(pdf_url, pdf_path):
    """Download a single paper, with retries on failure."""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(pdf_url, timeout=10)
            response.raise_for_status()
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Successfully downloaded: {pdf_url}")
            return
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for {pdf_url}. Reason: {e}")
            time.sleep(2)  # Backoff before retrying

    logging.error(f"Failed to download {pdf_url} after {MAX_RETRIES} attempts.")

def process_year(year):
    """Process all papers for a given year."""
    print(f'---- PROCESSING YEAR {year} ----')
    year_directory = f'papers/{year}'
    if not os.path.exists(year_directory):
        os.makedirs(year_directory)

    # Fetch paper list for the year
    response = requests.get(BASE_URL + str(year))
    soup = BeautifulSoup(response.content, 'lxml')
    list_of_paper_links = soup.find_all('a', title='paper title')

    tasks = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for a in tqdm(list_of_paper_links, desc=f'Downloading {year} papers', unit='paper'):
            paper_link_components = a.get('href').split('/')[-1].split('-')
            paper_hash = paper_link_components[0]
            paper_link_base_url = BASE_URL + str(year) + '/file/' + paper_hash

            # Construct the PDF URL and filename
            if year >= 2022:
                paper_suffix = paper_link_components[2].split('.')[0]
                pdf_url = f"{paper_link_base_url}-Paper-{paper_suffix}.pdf"
                pdf_filename = f"{paper_hash}-Paper-{paper_suffix}.pdf"
            else:
                pdf_url = f"{paper_link_base_url}-Paper.pdf"
                pdf_filename = f"{paper_hash}-Paper.pdf"

            pdf_path = os.path.join(year_directory, pdf_filename)

            # If the paper hasn't been downloaded, schedule it for download
            if not os.path.exists(pdf_path):
                task = executor.submit(download_paper, pdf_url, pdf_path)
                tasks.append(task)

        # Wait for all downloads to complete
        for task in as_completed(tasks):
            task.result()  # Handle any exceptions raised during download

def main():
    for year in range(1987, 2024):
        process_year(year)

if __name__ == "__main__":
    main()
