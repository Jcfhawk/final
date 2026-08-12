from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from ml import send_message
import re
import os
from datetime import datetime
from urllib.parse import urlparse, urljoin

# Remove this section after done with ml training dataset
def finish_link(press_release, newsroom):
    if press_release.startswith("https://") or press_release.startswith("http://"):
        return str(press_release)
    elif press_release.startswith("/"):
        parsed_url = urlparse(newsroom)
        relevant_url = f"{parsed_url.scheme}://{parsed_url.netloc}{press_release}"
        return relevant_url
    elif not press_release.startswith(("#", "/", "https://", "http://")):
        full_url = urljoin(newsroom, press_release)
        return full_url
    elif press_release.startswith("#"):
        full_url = urljoin(newsroom, press_release)
        return full_url
    else:
        full_url = urljoin(newsroom, press_release)
        return full_url


extr_companies = [
    "Acacia Research Corporation",
    "Alimera Sciences, Inc",
    "American Resources Corporation",
    "Dominari Holdings Inc",
    "Eastern Company (The)",
    "The First of Long Island Corporation",
    "Friedman Industries Inc",
    "HireQuest, Inc",
    "Jerash Holdings (US), Inc",
    "LightPath Technologies, Inc",
    "Mill City Ventures III, Ltd",
    "Monogram Technologies Inc",
    "Maison Solutions Inc",
    "Insperity, Inc",
    "Pro-Dex, Inc",
    "Pedevco Corp",
    "Protagonist Therapeutics, Inc",
    "Sadot Group Inc",
    "Stabilis Solutions, Inc",
    "Simulations Plus, Inc",
    "Presidio Property Trust, Inc",
    "SWK Holdings Corporation",
    "urban-gro, Inc",
    "WidePoint Corporation",
    "Zedge, Inc",
    "Zomedica Corp"
]


def get_page(url, driver, company):
    try:
        driver.get(url)
        time.sleep(1)
    except Exception:
        time.sleep(1)
        try:
            driver.get(url)
            time.sleep(1)
        except Exception:

            return "Not Good"
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception:
        return "Not Good"

    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        iframe_contents = {}
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                iframe_html = driver.page_source
                iframe_contents[f"iframe_{index}"] = iframe_html
            except Exception as iframe_error:
                pass
            finally:
                driver.switch_to.default_content()

        html_content = f"<!-- Main Page HTML -->\n{soup.prettify()}\n\n"
        for iframe_name, iframe_html in iframe_contents.items():
            soup_iframe = BeautifulSoup(iframe_html, "html.parser")
            html_content += f"<!-- {iframe_name} HTML -->\n{soup_iframe.prettify()}\n\n"

        return html_content

    except Exception:
        return f"<!-- Main Page HTML -->\n{soup.prettify()}\n\n"


def get_links(company, content):
    file = f"C:\\final\\company_directives\\{company}\\links.txt"
    old_links = []
    new_links = []
    for_check_links = []
    query_titles = []
    soup = BeautifulSoup(content, "html.parser")
    if company in extr_companies:
        anchors = soup.find_all('div', class_="headline text-link")
        for anchor in anchors:
            if anchor.has_attr('onclick'):
                clean_href = anchor['onclick'].split("'")[1]
                new_links.append(clean_href.strip())
        with open(file, 'r', errors="ignore") as file5:
            for line in file5:
                link = line.strip().split('Link: ')[1]
                old_links.append(link.strip())
        links_to_write = list(set(new_links) - set(old_links))
        with open(file, 'a', errors="ignore") as file5:
            for anchor in anchors:
                clean_href1 = anchor['onclick'].split("'")[1]
                if clean_href1 in links_to_write:
                    one_title = anchor.get('title')
                    file5.write(f"Title: {one_title}, Link: {clean_href1}" + "\n")
                    for_check_links.append(f"Title: {one_title}, Link: {clean_href1}")
    else:
        new_links = {}
        anchors = soup.find_all('a')
        for anchor in anchors:
            if anchor.get('href'):
                clean_href = anchor.get('href').replace("\n", "").strip()
                clean_href = re.sub(r"[\u200B\u200C\u200D\u202F\uFEFF]", "", clean_href)
                text = anchor.get_text(strip=True)

                if clean_href not in new_links or (new_links[clean_href] == "" and text != ""):
                    new_links[clean_href] = text

        new_links_list = list(new_links.keys())
        old_links = []
        with open(file, 'r', errors="ignore") as file5:
            for line in file5:
                if 'Link: ' in line:
                    link = line.strip().split('Link: ')[1]
                    old_links.append(link.strip())
        links_to_write = list(set(new_links_list) - set(old_links))
        with open(file, "r", errors="ignore") as file6:
            for line in file6:
                query_titles.append(line.strip().split(" ,Link:")[0].split("Title: ")[1].strip())
        for ltw in links_to_write:
            if "?" in ltw and ltw.split("?")[1].strip():
                link_text = new_links.get(ltw, "").strip()
                normalized_title = " ".join(link_text.split())
                if normalized_title in query_titles:
                    links_to_write.remove(ltw)
        with open(file, 'a', errors="ignore") as file5:
            for anchor in anchors:
                if anchor.get('href') in links_to_write:
                    link_title = anchor.get_text(strip=True)
                    if link_title == "":
                        continue
                    one_title = " ".join(link_title.split())
                    clean_href1 = anchor.get('href').replace("\n", "").strip()
                    clean_href2 = re.sub(r"[\u200B\u200C\u200D\u202F\uFEFF]", "", clean_href1)
                    file5.write(f"Title: {one_title}, Link: {clean_href2}" + "\n")
                    for_check_links.append(f"Title: {one_title}, Link: {clean_href2}")
    return for_check_links


def check_links(company, links_to_check, ticker, newsroom, multilist, row):
    links = []
    link_directs = []
    file2 = f"C:\\final\\company_directives\\{company}\\press_release_links.txt"
    file4 = f"C:\\final\\company_directives\\{company}\\link_direct.txt"

    if os.path.isfile(file4):
        with open(file4, "r", errors="ignore") as file5:
            for line in file5:
                link_directs.append(line.strip())

    with open(file2, 'a', errors="ignore") as file3:
        for link_to_check in links_to_check:
            link_release = link_to_check.split("Link: ")[1].strip()
            press_release = re.sub(r"[\u200B\u200C\u200D\u202F\uFEFF]", "", link_release).strip()
            if press_release.startswith("#") or press_release.startswith("?"):
                continue
            if press_release not in links:
                links.append(press_release)
                title = link_to_check.split(", Link: ")[0].split("Title: ")[1].strip()
                link = link_to_check.split("Link: ")[1].strip()
                date = datetime.now().strftime("%m/%d/%y")
                time1 = datetime.now().strftime("%H:%M:%S")
                multilist.append(
                    {"Company": company, "Newsroom": newsroom, "Link": link,
                    "Title": title, "Ticker": ticker})
                to_send_message = {"Company": company, "Newsroom": newsroom, "Link": link, "Title": title,
                                   "Ticker": ticker, "Date": date, "Time": time1, "Term": row["Term"], "RE": row["RE"],
                                   "OG": row["OG"], "MRKTCAP": row["MRKTCAP"]}
                send_message(to_send_message)
                file3.write(link_to_check + "\n")


def restart_chrome(driv, driver_path, version, port, port2, x):
    x += 1
    time.sleep(1)
    if driv == "Driver 1":
        directory = "user1"
    elif driv == "Driver 2":
        directory = "user2"
    elif driv == "Driver 3":
        directory = "user3"
    else:
        directory = "user4"
    if x % 2 != 0:
        cmd = f'start chrome --remote-debugging-port={port2} --user-data-dir="C:/final/{directory}"'
        os.system(cmd)
        time.sleep(2)
        try:
            opts1 = Options()
            opts1.debugger_address = f"127.0.0.1:{port2}"
            opts1.add_argument("--headless")
            driver = uc.Chrome(use_subprocess=True, options=opts1, driver_executable_path=driver_path, version_main=version)
            driver.set_page_load_timeout(8)
            return driver
        except Exception as e:
            opts1 = Options()
            opts1.debugger_address = f"127.0.0.1:{port2}"
            opts1.add_argument("--headless")
            driver = uc.Chrome(use_subprocess=True, options=opts1, driver_executable_path=driver_path,
                               version_main=version)
            driver.set_page_load_timeout(8)
            return driver
    else:
        cmd = f'start chrome --remote-debugging-port={port} --user-data-dir="C:/final/{directory}"'
        os.system(cmd)
        time.sleep(2)
        try:
            opts2 = Options()
            opts2.debugger_address = f"127.0.0.1:{port}"
            opts2.add_argument("--headless")
            driver = uc.Chrome(use_subprocess=True, options=opts2, driver_executable_path=driver_path, version_main=version)
            driver.set_page_load_timeout(8)
            return driver
        except Exception as e:
            time.sleep(2)
            opts2 = Options()
            opts2.debugger_address = f"127.0.0.1:{port}"
            opts2.add_argument("--headless")
            driver = uc.Chrome(use_subprocess=True, options=opts2, driver_executable_path=driver_path,
                               version_main=version)
            driver.set_page_load_timeout(8)
            return driver


def scrape_section(df, port, driver_path, multilist, version, driv, port2):
    x = 0
    opts = Options()
    opts.debugger_address = f"127.0.0.1:{port}"
    opts.add_argument("--headless")
    driver = uc.Chrome(use_subprocess=True, options=opts, driver_executable_path=driver_path, version_main=version)
    driver.set_page_load_timeout(8)
    start_trading1 = 315
    end_trading1 = 510
    start_trading2 = 899
    end_trading2 = 960
    cur_trade_time = "Before"
    flag = False

    while True:
        now = time.localtime()
        current_time = now.tm_hour * 60 + now.tm_min

        if current_time > end_trading2:
            return
        elif current_time < start_trading1:
            driver.close()
            driver.quit()
            mtg = start_trading1 - current_time
            time.sleep(mtg * 60)
            flag = True
            continue
        elif end_trading1 < current_time < start_trading2:
            driver.close()
            driver.quit()
            mtg = start_trading2 - current_time
            time.sleep(mtg * 60)
            flag = True
            continue

        if current_time > start_trading2:
            cur_trade_time = "After"

        if flag:
            driver = restart_chrome(driv, driver_path, version, port, port2, x)
            flag = False

        try:
            start = time.time()
            for dic in range(len(df)):
                row = df.iloc[dic]
                if row["Hour"] != cur_trade_time:
                    continue
                company = row['Company'].rstrip(".")
                newsroom = row['Newsroom']
                ticker = row['Ticker']
                try:
                    html_content = get_page(newsroom, driver=driver, company=company)
                    if html_content == "Not Good":
                        continue
                    links_to_check = get_links(company, html_content)
                    check_links(company, links_to_check, ticker, newsroom, multilist, row)
                except Exception as e:
                    print(f"[{driv}] Error occurred: {e}")
                    continue
            driver.close()
            driver.quit()
            driver = restart_chrome(driv, driver_path, version, port, port2, x)
            end = time.time()
            print(f"{driv}: {end - start}")
        except Exception as e:
            print(f"[{driv}] Error occurred: {e}")
            continue










