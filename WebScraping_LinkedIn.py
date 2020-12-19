from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

company1, position1, employment_dates1, company2, position2, employment_dates2, full_name, linkedin_url = [], [], [], [], [], [], [], []
df = pd.read_excel(r'path to input file with first name and last name')
input_fname = df['First Name'].values.tolist()
input_lname = df['Last Name'].values.tolist()

count = len(input_fname)

''' Logging in to LinkedIn '''
driver = webdriver.Chrome(
    executable_path=r'path to chromedriver.exe')
driver.get("https://www.linkedin.com/login")
uname = driver.find_element_by_xpath('//*[@id="username"]')
uname.send_keys("email_id@email.com")
time.sleep(5)
password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys("linkedin account password")
time.sleep(3)
password.submit()

for i in range(count):
    if i % 15 == 0:
        time.sleep(5)

    search_query = input_fname[i] + " AND " + input_lname[i] + " AND searchkey1 AND searchkey2 AND site:linkedin.com" #search person with required filters
    # print(search_query)
    time.sleep(10)

    ''' open google and search person with required fields '''
    driver.get("https://www.google.com/")
    query = driver.find_element_by_xpath('//*[@class="gLFyf gsfi"]')
    time.sleep(5)
    query.send_keys(search_query)
    time.sleep(2)
    query.submit()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html')
    class_info = soup.find('div', class_='yuRUbf')
    name = input_fname[i] + " " + input_lname[i]

    try:
        url = class_info.a['href']
        # print(url)

    except:
        linkedin_url.append(" ")
        company1.append(" ")
        position1.append(" ")
        employment_dates1.append(" ")
        company2.append(" ")
        position2.append(" ")
        employment_dates2.append(" ")
        full_name.append(name)
        continue
    linkedin_url.append(url)
    full_name.append(name)

    time.sleep(3)
    try:
        driver.get(url)
    except:
        continue
    driver.implicitly_wait(5)

    ''' scraping top 2 experiences of individual '''
    soup1 = BeautifulSoup(driver.page_source, 'html')
    experience = soup1.find(id="experience-section")
    if experience is not None:
        recent_experiences = experience.findAll("li")
        if recent_experiences[0].find("ul") is not None:
            try:
                com_1 = recent_experiences[0].find("h3", class_="t-16 t-black t-bold").text.split("\n")[2]
            except:
                com_1 = ""
            multiple_positions = recent_experiences[0].findAll("li")[:2]
            try:
                pos_1 = multiple_positions[0].find("h3", class_="t-14 t-black t-bold").text.split("\n")[2]
            except:
                pos_1 = ""
            try:
                dur_1 = multiple_positions[0].find("h4",
                                                   class_="pv-entity__date-range t-14 t-black--light t-normal").text.split(
                    "\n")[2]
            except:
                dur_1 = ""
            com_2 = com_1
            try:
                pos_2 = multiple_positions[1].find("h3", class_="t-14 t-black t-bold").text.split("\n")[2]
            except:
                pos_2 = ""
            try:
                dur_2 = multiple_positions[1].find("h4",
                                                   class_="pv-entity__date-range t-14 t-black--light t-normal").text.split(
                    "\n")[2]
            except:
                dur_2 = ""

            company1.append(com_1)
            position1.append(pos_1)
            employment_dates1.append(dur_1)
            company2.append(com_2)
            position2.append(pos_2)
            employment_dates2.append(dur_2)

            # print("first if", com_1, pos_1, dur_1, com_2, pos_2, dur_2)

            continue

        else:
            try:
                com_1 = recent_experiences[0].find("p",class_="pv-entity__secondary-title t-14 t-black t-normal").text.split(
                        "\n")[1].strip()
            except:
                com_1 = ""
            try:
                pos_1 = recent_experiences[0].find("h3", class_="t-16 t-black t-bold").text.split("\n")[0]
            except:
                pos_1 = ""
            try:
                dur_1 = recent_experiences[0].find("h4",
                                                   class_="pv-entity__date-range t-14 t-black--light t-normal").text.split(
                    "\n")[2]
            except:
                dur_1 = ""

        if len(recent_experiences) > 1 and recent_experiences[1].find("ul") is not None:
            try:
                com_2 = recent_experiences[1].find("h3", class_="t-16 t-black t-bold").text.split("\n")[2]
            except:
                com_2 = ""
            try:
                pos_2 = recent_experiences[1].find("h3", class_="t-14 t-black t-bold").text.split("\n")[2]
            except:
                pos_2 = ""
            try:
                dur_2 = recent_experiences[1].find("h4",
                                                   class_="pv-entity__date-range t-14 t-black--light t-normal").text.split(
                    "\n")[2]
            except:
                dur_2 = ""
        else:
            try:
                com_2 = \
                    recent_experiences[1].find("p",
                                               class_="pv-entity__secondary-title t-14 t-black t-normal").text.split(
                        "\n")[1].strip()
            except:
                com_2 = ""
            try:
                pos_2 = recent_experiences[1].find("h3", class_="t-16 t-black t-bold").text.split("\n")[0]
            except:
                pos_2 = ""
            try:
                dur_2 = recent_experiences[1].find("h4",
                                                   class_="pv-entity__date-range t-14 t-black--light t-normal").text.split(
                    "\n")[2]
            except:
                dur_2 = ""

        # print("outside if", com_1, pos_1, dur_1, com_2, pos_2, dur_2)
        company1.append(com_1)
        position1.append(pos_1)
        employment_dates1.append(dur_1)
        company2.append(com_2)
        position2.append(pos_2)
        employment_dates2.append(dur_2)
    else:
        company1.append(" ")
        position1.append(" ")
        employment_dates1.append(" ")
        company2.append(" ")
        position2.append(" ")
        employment_dates2.append(" ")
driver.quit()

output = {"Name": full_name, "URL": linkedin_url, "Position1": position1, "Company1": company1,
          "Duration1": employment_dates1, "Position2": position2, "Company2": company2, "Duration2": employment_dates2}
df1 = pd.DataFrame(output)
df1.to_excel(r'output file.xlsx', index=False)
