import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://devgan.in/"
main_url = "https://devgan.in/all_sections_ipc.php"

response = requests.get(main_url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

content_div = soup.find("div", id="content")

ipc_data = []

for link in content_div.find_all("a"):
    ipc_code = link.text.strip()
    sub_url = link.get('href')
    full_url = base_url + sub_url

    sub_response = requests.get(full_url)
    sub_response.raise_for_status()

    sub_soup = BeautifulSoup(sub_response.content, "html.parser")

    search_div = sub_soup.find("div", class_="search")

    title, description = "", ""
    if search_div:
        title_row = search_div.find("tr", class_="mys-head")
        if title_row:
            tds = title_row.find_all("td")
            if len(tds) > 1 and tds[1].find("h2"):
                title = tds[1].find("h2").text.strip()

        description_row = search_div.find("tr", class_="mys-desc")
        if description_row and description_row.find("p"):
            description = description_row.find("p").text.strip()

        print(f"Appending data: IPC Code: {ipc_code}, Title: {title}, Description: {description}")
        ipc_data.append([ipc_code, title, description])

    time.sleep(1)

with open("ipc_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["IPC Code", "Title", "Description"])
    writer.writerows(ipc_data)

