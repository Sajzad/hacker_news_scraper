"""
HN Frontpage Parser
===================

    Description:
        parse hn front page and collect's titles, links, comment links and votes
    Dependency:
        requests
        bs4
        pandas
    Output:
        a csv file containing the column: title, link, comment, vote
"""
import requests
from bs4 import BeautifulSoup
# import pandas as pd

base_url = ""
# output_file = "hn_scraped_result.csv"

response = requests.get(base_url + "news")
content = response.content
soup = BeautifulSoup(content, "lxml")


titles, links, votes, comments = [], [], [], []
for tr in soup.find("table", {"class": "itemlist"}).find_all("tr"):
    if tr.attrs.get("class") and tr.attrs.get("class")[-1] == "athing":
        # parse title & link
        if tr.find_all("td", {"class", "title"}):
            td = tr.find_all("td", {"class", "title"})[-1]
            titles.append(td.find("a").get_text())
            links.append(td.find("a").attrs.get("href"))
            print(td.find("a").get_text())
    # elif tr.attrs.get("class") == "spacer":
        # ignore empty td
        continue
    else:
        # parse votes & comment link
        td = tr.find("td", {"class", "subtext"})
        if td:
            comment_link = td.find_all("a")[-1]["href"]
            # append relative link with base url to make absolute url
            comments.append(base_url + comment_link)
            print(comment_link)
            if td.find("span"):
                vote = td.find("span").text.replace("points", "")
                votes.append(vote)
                print(vote)


data = []
for title, link, vote, comment_link in zip(titles, links, votes, comments):
    data.append({
        "title": title,
        "link": link,
        "vote": vote,
        "comment": comment_link
    })

if data:
    df = pd.DataFrame(columns=["title", "link", "vote", "comment"])
    df = df.append(data, ignore_index=True)
    df.to_csv(output_file, index=False)
