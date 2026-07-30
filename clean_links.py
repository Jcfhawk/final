from urllib.parse import urlparse, urljoin
import time
from bs4 import BeautifulSoup
import re
import glob
import os
import fitz
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
ban_list = ["next", "Next", "NEXT", "previous", "Previous", "PREVIOUS"]
ban_list2 = []
good_lines = []
bad_titles = [
    "read more",
    "pdf",
    "",

]


def get_structured_visible_text(soup):

    def format_table_as_markdown(table):
        rows = table.find_all('tr')  # Find all rows
        table_data = []

        for row in rows:
            cells = row.find_all(['th', 'td'])  # Include both header and data cells
            # Clean each cell's text and ignore completely empty cells
            row_data = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]
            table_data.append(row_data)

        # Ensure each row has at least one valid cell before processing
        table_data = [row for row in table_data if row]

        if not table_data:  # If the table is empty after cleaning
            return ""

        # Find the maximum number of columns in any row for alignment
        max_columns = max(len(row) for row in table_data)

        # Ensure all rows have the same number of columns by filling missing cells with empty strings
        normalized_data = [row + [""] * (max_columns - len(row)) for row in table_data]

        # Format the table rows into Markdown
        markdown_rows = [" ".join(row) for row in normalized_data]

        # Add a Markdown header separator if the first row looks like a header (contains no numeric data)
        if any(cell.isalpha() for cell in normalized_data[0]):
            header_separator = " | ".join(["---"] * max_columns)
            markdown_rows.insert(1, header_separator)

        return "\n".join(markdown_rows)

    imgs = soup.find_all('img')
    for img in imgs:
        img_text = img.get('alt')
        if img_text:
            ban_list.append(img_text)

    for heading_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        ban_list.append(heading_tag.get_text(strip=True))

    for tag in soup(
            ['style', 'script', 'head', 'title', 'meta', 'img', 'picture', 'figure', 'footer', 'h1', 'h2', 'h3', 'h4',
             'h5', 'h6', 'button']):
        tag.decompose()

    # Process tables separately and replace them with Markdown in the soup
    tables = soup.find_all('table')
    for table in tables:
        markdown_table = format_table_as_markdown(table)
        table.replace_with(f"\n{markdown_table}\n")  # Replace the table with its Markdown representation

    for element in soup.find_all(True):
        if not element.get_text(strip=True):
            element.decompose()

    return soup


def clean_text(text):
    text = re.sub(r'[ \t]+', ' ', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = re.sub(r'\n+', '\n', text).strip()
    return text


def get_text_article(new_soup):
    get_text = new_soup.get_text()
    return get_text


def split_parts(cleaned_text):
    parts = cleaned_text.split("\n")
    return parts


def find_unique_parts(parts1, parts2):
    full_article = []
    unique_parts = [part for part in parts1 if part not in parts2 and part not in ban_list]

    for line in parts1:
        if line in unique_parts and line not in ban_list:
            full_article.append(line)
            ban_list.append(line)

    return full_article


def replace_html(company, html_content):
    press_release_html1 = f"C:\\Users\\Hawki\\OneDrive\\Desktop\\trading setup\\company_directories\\{company}\\press_release_dir\\press_release1.html"
    with open(press_release_html1, "w", encoding="utf-8") as file:
        file.write(html_content)


def read_existing_article(company):
    press_release_html1 = f"C:\\Users\\Hawki\\OneDrive\\Desktop\\trading setup\\company_directories\\{company}\\press_release_dir\\press_release1.html"
    with open(press_release_html1, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


def soup_article(html_content):
    soup1 = BeautifulSoup(html_content, "html.parser")
    return soup1


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


def get_article(url, driver):
    url = url
    try:
        driver.get(url)
        time.sleep(3)
    except Exception as e:
        time.sleep(3)
    html_content1 = driver.page_source
    return html_content1


def get_title(soup):
    for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        heading = soup.find(tag)
        if heading:
            if heading.text.strip().lower() in bad_titles:
                continue
            else:
                return heading.text.strip()
    return "No Title"


def check_pdf(link):
    if link.endswith(".pdf") or link.endswith("/pdf"):
        return "PDF"
    else:
        return "Webpage"


def get_article_pdf(link, driver):
    download_path = f"C:\\Users\\Hawki\\OneDrive\\Desktop\\pdfs"
    driver.get(link)
    driver.execute_script("window.print();")
    time.sleep(1)
    list_of_files = glob.glob(f"{download_path}/*.pdf")
    if list_of_files:
        try:
            latest_file = max(list_of_files, key=os.path.getctime)
        except Exception as e:
            time.sleep(1)
            latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    else:
        time.sleep(2)
        list_of_files = glob.glob(f"{download_path}/*.pdf")
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


def extract_and_merge_text(pdf_path):
    ban_spans = ["®", "", "™", "Contact:", "NEWS RELEASE", "News Release", "th", "Press Contact:",
                 "FOR IMMEDIATE RELEASE", "Repli", "Press Release", "N e w s   R e l e a s e", "News",
                 "For Media Inquiries", "FORM 10-K", "E E", "Gen", "NEWS", "1", "Table of Contents", "E" ,"•"]
    pot_titles = []
    mean_fonts = []
    x = {}
    y = 0
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text_blocks = page.get_text("dict")

            merged_text = []
            last_span = None

            for block in text_blocks["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text.strip() in ban_spans:
                            continue
                        font_size = span.get("size", 0)
                        font_name = span.get("font", "")

                        is_bold = "bold" in font_name.lower()

                        if last_span and last_span["font_size"] == font_size and last_span["is_bold"] == is_bold:
                            last_span["text"] += " " + text
                        else:
                            if last_span:
                                merged_text.append(last_span)
                            last_span = {
                                "text": text,
                                "font_size": font_size,
                                "is_bold": is_bold
                            }
            if last_span:
                merged_text.append(last_span)

            if len(merged_text) == 0:
                return "PDF File Corrupted"

            for item in merged_text:
                mean_fonts.append({"text": item['text'].strip(), "size": round(item['font_size']), "page": page_num, "bold": 'Yes' if item['is_bold'] else 'No'})
    for font in mean_fonts:
        size = font['size']
        y += size
        if size in x:
            x[size] += 1
        else:
            x[size] = 1
    max_count = max(x.values())
    mode = [num for num, count in x.items() if count == max_count]
    for font in mean_fonts:
        size = font['size']
        mean_font_page_num = font['page']
        if size > max(mode) and mean_font_page_num == 1:
            pot_titles.append(font)
    try:
        max_size = max(font['size'] for font in pot_titles)
        max_size_titles = [font for font in pot_titles if font['size'] == max_size]
        rtitle = next((font['text'].strip() for font in max_size_titles if font.get('bold') == "Yes"),
                      max_size_titles[0]['text'].strip())
        return rtitle
    except Exception as e:
        try:
            rtitle = next((font['text'].strip() for font in mean_fonts if font.get('bold') == "Yes"),
                      mean_fonts[0]['text'].strip())
            return rtitle
        except Exception as e:
            rtitle = mean_fonts[0]['text']
            return rtitle


def launch_chrome():
    cmd = f"start chrome --remote-debugging-port=6666 --user-data-dir=C:\\user1\\instancedata_38"
    os.system(cmd)
    opts = Options()
    opts.debugger_address = f"127.0.0.1:6666"
    opts.add_argument("--headless")
    driver = uc.Chrome(use_subprocess=True, options=opts, driver_executable_path="C:\\drivers\\chromedriver7.exe")
    return driver



def article(press_release_dict, driver1):
    company = press_release_dict['Company']
    newsroom = press_release_dict['Newsroom']
    press_release = press_release_dict['Link']
    link = finish_link(press_release, newsroom)
    article1 = get_article(link, driver1)
    soup_art = soup_article(article1)
    new_soup = get_structured_visible_text(soup_art)
    get_text = get_text_article(new_soup)
    cleaned_text = clean_text(get_text)
    parts = split_parts(cleaned_text)
    soup2 = read_existing_article(company)
    new_soup2 = get_structured_visible_text(soup2)
    get_text2 = new_soup2.get_text()
    cleaned_text2 = clean_text(get_text2)
    parts2 = split_parts(cleaned_text2)
    full_art = find_unique_parts(parts, parts2)
    replace_html(company, article1)
    return full_art


def article2(press_release_dict, driver1):
    newsroom = press_release_dict['Newsroom']
    press_release = press_release_dict['Link']
    link = finish_link(press_release, newsroom)
    types = check_pdf(link)
    if types == "PDF":
        art1 = get_article_pdf(link, driver1)
        pdf_title = extract_and_merge_text(art1)
        return pdf_title
    elif types == "Webpage":
        title = press_release_dict["Title"]
        if title.lower() in bad_titles:
            article1 = get_article(link, driver1)
            soup_art = soup_article(article1)
            title = get_title(soup_art)
            return title
        else:
            return title
