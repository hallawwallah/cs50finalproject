
from bs4 import BeautifulSoup
import re
import requests
from csv import writer
import pandas as pd

keywords = []

url = "https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,5"
urls = ["https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q={}&btnG=", "https://www.researchgate.net/search/publication?q={}",
        "https://www.semanticscholar.org/search?q={}&sort=relevance", "https://eric.ed.gov/?q={}", "https://www.academia.edu/search?q={}&utf8=%E2%9C%93"]

papers = []


def main():
    keywords = ask_keywords()
    # scrape the first 5 pages of google scholar for the selected paper results
    for i in range(0, 10):
        page = requests.get(url.format(i, keywords))
        soup = BeautifulSoup(page.content, "html.parser")
        divs = soup.findAll("div", class_="gs_r gs_or gs_scl")
        # with open("papers.csv", "w", encoding="utf8", newline="") as f:
        #cursor = writer(f)
        headers = ["title", "link to paper", "web source"]
        #cursor.writerow(headers)
        for div in divs:
            object = div.find("h3", class_="gs_rt")
            title = object.find("a").text
            web_source = soup.find("title").text
            # link_list.append(title)

            link = div.find('a', attrs={'href': re.compile("^https://")})
            paper_infos = [title, link.get("href"), web_source]
            papers.append(paper_infos)
    df = pd.DataFrame(papers, columns=headers)
    df.to_csv("papers_all")


def ask_keywords():
    question = input("what do you want to search? Type in some keywords: ")
    keywords.append(question)
    while not keywords:
        ask_keywords()
    print("search values:", keywords, "ready to go? (Y/N)")
    response = input()
    if response != "Y":
        ask_keywords()
    return keywords


if __name__ == "__main__":
    main()
