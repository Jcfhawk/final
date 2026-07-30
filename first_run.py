import os
import time
from pathlib import Path
import pandas as pd
import random


def make_directs(comp1, comp2, comp3, comp4):
    df1 = pd.read_csv(comp1)
    df2 = pd.read_csv(comp2)
    df3 = pd.read_csv(comp3)
    df4 = pd.read_csv(comp4)

    companies1 = df1['Company']
    companies2 = df2['Company']
    companies3 = df3['Company']
    companies4 = df4['Company']


    base_path = Path("C:/final/company_directives")

    for company in companies1:
        company_folder = base_path / company
        company_folder.mkdir(parents=True, exist_ok=True)
        (company_folder / "html_file1.html").touch()
        (company_folder / "html_file2.html").touch()
        (company_folder / "links.txt").touch()
        (company_folder / "press_release_links.txt").touch()

    for company in companies2:
        company_folder = base_path / company
        company_folder.mkdir(parents=True, exist_ok=True)
        (company_folder / "html_file1.html").touch()
        (company_folder / "html_file2.html").touch()
        (company_folder / "links.txt").touch()
        (company_folder / "press_release_links.txt").touch()

    for company in companies3:
        company_folder = base_path / company
        company_folder.mkdir(parents=True, exist_ok=True)
        (company_folder / "html_file1.html").touch()
        (company_folder / "html_file2.html").touch()
        (company_folder / "links.txt").touch()
        (company_folder / "press_release_links.txt").touch()

    for company in companies4:
        company_folder = base_path / company
        company_folder.mkdir(parents=True, exist_ok=True)
        (company_folder / "html_file1.html").touch()
        (company_folder / "html_file2.html").touch()
        (company_folder / "links.txt").touch()
        (company_folder / "press_release_links.txt").touch()

def first_run_check():
    config_path = Path("C:/final/config.txt")
    user_data1 = Path("C:/final/user1")
    user_data2 = Path("C:/final/user2")
    user_data3 = Path("C:/final/user3")
    user_data4 = Path("C:/final/user4")
    comp1 = Path("C:/final/company_directives")

    if config_path.exists():
        with open(config_path, "r") as file:
            for line in file:
                if line.startswith("Driver 1:"):
                    driver1 = line.split(": ")[1].strip()
                elif line.startswith("Driver 2:"):
                    driver2 = line.split(": ")[1].strip()
                elif line.startswith("Driver 3:"):
                    driver3 = line.split(": ")[1].strip()
                elif line.startswith("Driver 4:"):
                    driver4 = line.split(": ")[1].strip()
                elif line.startswith("Company List 1:"):
                    company1 = line.split("Company List 1: ")[1].strip()
                elif line.startswith("Company List 2:"):
                    company2 = line.split("Company List 2: ")[1].strip()
                elif line.startswith("Company List 3:"):
                    company3 = line.split("Company List 3: ")[1].strip()
                else:
                    company4 = line.split(": ")[1].strip()
        print("Starting Money Maker $")
        return driver1, driver2, driver3, driver4, company1, company2, company3, company4
    else:
        driver1 = input("What is the path for the first driver?")
        driver2 = input("What is the path for the second driver?")
        driver3 = input("What is the path for the third driver?")
        driver4 = input("What is the path for the fourth driver?")
        company_list1 = input("What is the file for the first companies?")
        company_list2 = input("What is the file for the second companies?")
        company_list3 = input("What is the file for the third companies?")
        company_list4 = input("What is the file for the fourth companies?")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        user_data1.mkdir(parents=True, exist_ok=True)
        user_data2.mkdir(parents=True, exist_ok=True)
        user_data3.mkdir(parents=True, exist_ok=True)
        user_data4.mkdir(parents=True, exist_ok=True)
        comp1.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            f.write(f"Driver 1: {driver1}" + "\n")
            f.write(f"Driver 2: {driver2}" + "\n")
            f.write(f"Driver 3: {driver3}" + "\n")
            f.write(f"Driver 4: {driver4}" + "\n")
            f.write(f"Company List 1: {company_list1}" + "\n")
            f.write(f"Company List 2: {company_list2}" + "\n")
            f.write(f"Company List 3: {company_list3}" + "\n")
            f.write(f"Company List 4: {company_list4}" + "\n")
        make_directs(company_list1, company_list2, company_list3, company_list4)
        print("Starting Money Maker $")
        return driver1, driver2, driver3, driver4, company_list1, company_list2, company_list3, company_list4


def pandas_companies(comp1, comp2, comp3, comp4):
    df1 = pd.read_csv(comp1)

    df2 = pd.read_csv(comp2)

    df3 = pd.read_csv(comp3)

    df4 = pd.read_csv(comp4)

    return df1, df2, df3, df4


def ports():
    port1 = random.randint(5000, 8000)
    port2 = random.randint(5000, 8000)
    port3 = random.randint(5000, 8000)
    port4 = random.randint(5000, 8000)
    port5 = random.randint(5000, 8000)
    port6 = random.randint(5000, 8000)
    port7 = random.randint(5000, 8000)
    port8 = random.randint(5000, 8000)
    if port1 != port2:
        cmd1 = f'start chrome --remote-debugging-port={port1} --user-data-dir="C:/final/user1"'
        cmd2 = f'start chrome --remote-debugging-port={port2} --user-data-dir="C:/final/user2"'
        cmd3 = f'start chrome --remote-debugging-port={port3} --user-data-dir="C:/final/user3"'
        cmd4 = f'start chrome --remote-debugging-port={port4} --user-data-dir="C:/final/user4"'
        os.system(cmd1)
        time.sleep(1)
        os.system(cmd2)
        time.sleep(1)
        os.system(cmd3)
        time.sleep(1)
        os.system(cmd4)
        return port1, port2, port3, port4, port5, port6, port7, port8
    else:
        port2 = port1 + 1
        cmd1 = f'start chrome --remote-debugging-port={port1} --user-data-dir="C:/final/user1"'
        cmd2 = f'start chrome --remote-debugging-port={port2} --user-data-dir="C:/final/user2"'
        cmd3 = f'start chrome --remote-debugging-port={port3} --user-data-dir="C:/final/user3"'
        cmd4 = f'start chrome --remote-debugging-port={port4} --user-data-dir="C:/final/user4"'
        os.system(cmd1)
        time.sleep(0.5)
        os.system(cmd2)
        time.sleep(0.5)
        os.system(cmd3)
        time.sleep(0.5)
        os.system(cmd4)
        return port1, port2, port3, port4, port5, port6, port7, port8
