
from bs4 import BeautifulSoup
import re
import requests
from csv import writer

keywords = []

url = "https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q={}&btnG="
urls = ["https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q={}&btnG=", "https://www.researchgate.net/search/publication?q={}", "https://www.semanticscholar.org/search?q={}&sort=relevance", "https://eric.ed.gov/?q={}", "https://www.academia.edu/search?q={}&utf8=%E2%9C%93"]

def main():
    keywords = ask_keywords()
    page = requests.get(url.format(keywords))
    # driver.get(url.format(keywords))
    #content = page.encode("utf-8")
    soup = BeautifulSoup(page.content, "html.parser")
    papers = soup.findAll("div", class_="gs_r gs_or gs_scl")
    # print(titles)
    #link_list = []
    paper_link = {}
    with open("papers.csv", "w", encoding="utf8", newline="") as f:
        cursor = writer(f)
        headers = ["title", "link to paper", "web source"]
        cursor.writerow(headers)
        for paper in papers:
            object = paper.find("h3", class_="gs_rt")
            title = object.find("a").text
            web_source = soup.find("title").text
        # link_list.append(title)
            link = paper.find('a', attrs={'href': re.compile("^https://")})
            paper_infos = [title, link.get("href"), web_source]
            cursor.writerow(paper_infos)
            

    print(paper_link)

#page = requests.get(url)

# print(page)

#soup = BeautifulSoup(page.content, "html.parser")
# print(soup)
#videos = soup.find_all("yt-formatted-string", class_="style-scope ytd-rich-grid-media")


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
