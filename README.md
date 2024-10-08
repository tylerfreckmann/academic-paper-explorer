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

You can view a preview of the data in this repository: [papers_tail.csv](https://github.com/tylerfreckmann/academic-paper-explorer/blob/main/papers_tail.csv).

The full dataset is stored in an AWS S3 bucket. You can download a CSV version of the data or a compressed CSV at the following links _(but please note the size of data before downloading)_.

 - `papers.csv` ~1GB : https://academic-paper-explorer.s3.us-east-2.amazonaws.com/papers.csv
 - `papers.csv.gzip` ~300MB : https://academic-paper-explorer.s3.us-east-2.amazonaws.com/papers.csv.gz

## Next Steps

The next steps for this project include more feature engineering like creating columns for the papers' abstracts, authors, and potentially citations. Additionally, it may be helpful to further "chunk" the papers into their different sections.

After that, Generative AI and NLP techniques will be applied to the collection of papers to make them easier to explore. Techniques will include Retrieval-Augmented Generation in a Q&A bot, search, and paper suggestions via semantic similarity analysis.

Stay tuned for more!
