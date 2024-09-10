# Academic Paper Explorer

This project will explore how Generative AI and NLP can be used to make navigating a collection of academic papers easier for end users.

## Collecting the Data

The data used in this project comes from the [NeurIPS Conference Proceedings](https://papers.nips.cc/).

All papers from 1987-2023 have been downloaded and stored in a CSV file on AWS S3. The CSV file is ~1 GB in size and contains ~20,000 rows. Each row contains three columns:

 - `year` - the year the paper was published
 - `name` - the title of the paper
 - `text` - the full text of the paper

[paper-scraper.py](https://github.com/tylerfreckmann/academic-paper-explorer/blob/main/paper-scraper.py) scrapes this data from the [NeurIPS Conference Proceedings website](https://papers.nips.cc/).

For years <= 2019, the conference website provides a `metadata.json` link for each paper that contains the paper's full text in a JSON object.

For years >= 2020, only the paper PDFs are provided, so `paper-scraper.py` downloads the PDFs and uses [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/index.html) to convert the PDFs into plain text.

Once all papers have been downloaded and processed, they are stored in a Pandas DataFrame and saved to a CSV.

### The Data File

The data is stored in an AWS S3 bucket. You can download a CSV version of the data or a compressed CSV at the following links _(but please note the size of data before downloading)_.

 - `papers.csv`: https://academic-paper-explorer.s3.us-east-2.amazonaws.com/papers.csv ~1 GB
 - `papers.csv.gzip`: https://academic-paper-explorer.s3.us-east-2.amazonaws.com/papers.csv.gz ~300MB
