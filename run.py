from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import csv
import os
import sys
import spacy
import subprocess
import time


def download_spacy_model(model_name="en_core_web_sm"):
    try:
        spacy.load(model_name)
        print(f"{model_name} is already downloaded.")
    except:
        print(f"{model_name} not found. Downloading...")
        cmd = f"python -m spacy download {model_name}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"{model_name} downloaded successfully.")
    return model_name


def main(model_name):
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} START END(NOT INCLUDE)")

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    if os.environ.get("START_URL_FILE"):
        with open(os.environ.get("START_URL_FILE"), encoding="utf-8-sig") as f:
            start_time = time.time() 
            i = 0
            n_crawlers = 0
            process = CrawlerProcess(get_project_settings())
            ner_transformer = spacy.load(model_name)

            reader = csv.DictReader(f)
            for row in reader:
                if row["type"] not in ["npo", "both"]:
                    continue
                row["rank"] = row["ein"]
                u = row["website"]
                if u[:4] != "http":
                    u = "http://" + u
                if i >= start:
                    print(f"#### Create crawler for {i}: {urlparse(u).netloc}")
                    process.crawl(
                        "npos",
                        start_urls=[u],
                        npos={u: row},
                        transformer=ner_transformer,
                        allowed_domains=[urlparse(u).netloc],
                    )
                    n_crawlers = n_crawlers + 1
                i = i + 1
                if i >= end:
                    break
            if n_crawlers > 0:
                print(f"#### Run crawlers {start}-{start+n_crawlers-1}")
                process.start()
                print(f"#### End crawlers {start}-{start+n_crawlers-1}")
                # the script will block here until the crawling is finished
            end_time = time.time() 
            elapsed_time = end_time - start_time
            print("execution time:",elapsed_time)
    else:
        print("missing START_URL_FILE in environment variable")


if __name__ == "__main__":
    model_mame = download_spacy_model()
    main(model_mame)