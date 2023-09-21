import csv
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep
import run_parsing
import xpath_element

# Assigning variables from run_parsing module
login = run_parsing.login
password = run_parsing.password
delay = run_parsing.delay
id = run_parsing.id

# Initializing Selenium driver
driver = webdriver.Chrome()

# Checking for saved cookies
driver.get("https://www.linkedin.com/login")
driver.find_element(By.ID, "username").send_keys(login)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[text()='Log in']").click()

# Reading data from CSV file tsp_profile.csv
with open('tsp_profiles.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skipping headers

    # Opening a file for writing data
    with open('scrapped_profiles.csv', 'w', encoding='utf-8', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=";")
        headers = ['id', 'li_first_name', 'li_last_name', 'li_city_id', 'li_current_location', 'li_headline',
                   'li_alternative_location', 'li_company_name_and_location', 'li_skills', 'li_business_domain',
                   'li_positions', 'li_educations', 'li_certificates', 'li_languages']
        writer.writerow(headers)

        # Flag to determine whether to process profiles
        process_profiles = id is None  # Flag to determine if we should start processing profiles

        for row in reader:
            if not process_profiles:
                if row[0] == str(id):
                    process_profiles = True
            if not process_profiles:
                continue
            url = row[1]
            sleep(3)  # Delay before visiting each profile
            driver.get(url)
            try:
                # Extracting first name and last name
                try:
                    name_element = driver.find_element(By.XPATH, xpath_element.name_element)
                    name = name_element.text
                    li_first_name, li_last_name = name.split(' ', 1)
                except NoSuchElementException:
                    li_first_name = ""
                    li_last_name = ""

                # Extracting profile location
                try:
                    location_element = driver.find_element(By.XPATH, xpath_element.location_element)
                    current_location = location_element.text
                except NoSuchElementException:
                    current_location = ""


                # Function to compare cities
                def compare_cities(words, json_list):
                    matching_cities = []
                    for cities in json_list['cities']:
                        cities_name = cities['_source']['name']
                        if words.lower() == cities_name.lower():
                            matching_cities.append((cities_name, cities['_source']['id']))

                        # Checking matches among synonyms
                        for synonym in cities['_source']['synonyms']:
                            synonym_name = synonym['name']
                            if words.lower() == synonym_name.lower():
                                matching_cities.append((synonym_name, cities['_source']['id']))

                    return matching_cities


                # Function to analyze text and find cities
                def analyze_text(li_current_location, json_list):
                    words = re.findall(r'\w+', ' '.join([str(li_current_location)]).lower())
                    found_cities = []

                    for group_size in range(3, 0, -1):
                        for i in range(len(words) - group_size + 1):
                            group = ' '.join(words[i:i + group_size])
                            matched_cities = compare_cities(group, json_list)
                            if matched_cities:
                                found_cities.extend(matched_cities)

                    return found_cities


                with open('cities.json') as file:
                    json_list = json.load(file)

                found_cities = analyze_text(current_location, json_list)

                if found_cities:
                    li_current_location = found_cities[0][0]
                    li_city_id = found_cities[0][1]
                else:
                    li_current_location = current_location
                    li_city_id = None

                # Extracting alternative profile location
                try:
                    alternative_location_element = driver.find_element(By.XPATH,
                                                                       xpath_element.alternative_location_element)
                    li_alternative_location = alternative_location_element.text.split("·")[0].strip()
                    li_alternative_location_text = ', '.join(li_alternative_location).replace('[', '').replace(']', '')
                except NoSuchElementException:
                    li_alternative_location = ""

                # Extracting skills
                li_headline = driver.find_elements(By.XPATH, xpath_element.headline_element)
                li_headline = [element.text for element in li_headline]
                li_headline = ', '.join(li_headline).replace('[', '').replace(']', '')

                # Extracting positions
                try:
                    li_positions_text = driver.find_elements(By.XPATH, xpath_element.position_text_element)
                    li_positions_time = driver.find_elements(By.XPATH, xpath_element.position_time_element)
                    li_positions = []
                    for text, time in zip(li_positions_text, li_positions_time):
                        position_text = text.text
                        position_time = time.text.split('·')
                        position = f"{position_text} ({position_time})"
                        li_positions.append(position)
                    li_positions = ', '.join(li_positions)
                except NoSuchElementException:
                    li_positions = ""
                # Extracting education

                # Extracting education information
                try:
                    li_education_text = driver.find_elements(By.XPATH, xpath_element.education_text_elements)
                    li_education_time = driver.find_elements(By.XPATH, xpath_element.education_time_elements)
                    li_education = []
                    for text, time in zip(li_education_text, li_education_time):
                        education_text = text.text
                        education_time = time.text if time else ''
                        education = f"{education_text} ({education_time})"
                        li_education.append(education)
                    li_education = ', '.join(li_education) if li_education else ""
                except NoSuchElementException:
                    li_education = ""

                # Extracting certificates
                try:
                    li_certificate_text = driver.find_elements(By.XPATH, xpath_element.certificate_text_elements)
                    li_certificate_time = driver.find_elements(By.XPATH, xpath_element.certificate_time_elements)
                    li_certificate = []
                    for text, time in zip(li_certificate_text, li_certificate_time):
                        certificate_text = text.text
                        certificate_time = time.text
                        certificate = f"{certificate_text} ({certificate_time})"
                        li_certificate.append(certificate)
                    li_certificate = ', '.join(li_certificate)
                except NoSuchElementException:
                    li_certificate = ""

                # Extracting languages
                try:
                    li_languages_text = driver.find_elements(By.XPATH, xpath_element.languages_text_elements)
                    li_languages_level = driver.find_elements(By.XPATH, xpath_element.languages_level_elements)
                    li_languages = []
                    for text, level in zip(li_languages_text, li_languages_level):
                        languages_text = text.text
                        languages_level = level.text
                        languages = f"{languages_text} ({languages_level})"
                        li_languages.append(languages)
                    li_languages = ', '.join(li_languages)
                except NoSuchElementException:
                    li_languages = ""

                # Extracting skills
                try:
                    skills_subsequent = driver.find_elements(By.XPATH, xpath_element.skills_subsequent_elements)
                    skills_subsequent_text = [element.text for element in skills_subsequent]
                    skills_subsequent_2 = driver.find_elements(By.XPATH, xpath_element.skills_subsequent_2_elements)
                    skills_subsequent_2_text = [element.text for element in skills_subsequent_2]
                except NoSuchElementException:
                    skills_subsequent_text = ""
                    skills_subsequent_2_text = ""


                # Function to compare words and find matching skills
                def compare_words(words, json_data):
                    matching_skills = []
                    for skill in json_data['skills']:
                        skill_name = skill['_source']['name']
                        if words.lower() == skill_name.lower():
                            matching_skills.append(skill_name)

                    # Check for matches among synonyms
                    for skill in json_data['skills']:
                        synonyms = skill['_source']['synonyms']
                        for synonym in synonyms:
                            synonym_name = synonym['name']
                            # Check that the synonym word is in English
                            if all(c.isalpha() and ord(c) < 128 for c in
                                   synonym_name) and words.lower() == synonym_name.lower():
                                matching_skills.append(synonym_name)

                    return matching_skills


                # Function to analyze skills in text
                def analyze_text(skills_subsequent_text, skills_subsequent_2_text, json_data):
                    words = re.findall(r'\w+',
                                       ' '.join([str(skills_subsequent_text), str(skills_subsequent_2_text)]).lower())
                    found_skills = set()

                    for group_size in range(3, 0, -1):
                        for i in range(len(words) - group_size + 1):
                            group = ' '.join(words[i:i + group_size])
                            matched_skills = compare_words(group, json_data)
                            if matched_skills:
                                found_skills.update(matched_skills)

                    return found_skills


                # Read skills data from a JSON file
                with open('skills.json') as file:
                    json_data = json.load(file)

                # Analyze skills in the text
                found_skills = analyze_text(skills_subsequent_text, skills_subsequent_2_text, json_data)
                skills_str = ', '.join(found_skills)

                # Extracting business information
                try:
                    href_elements = driver.find_elements(By.XPATH, xpath_element.href_elements)
                    href_list = []
                    li_company_name_and_location = []
                    li_business_domain = []

                    for element in href_elements:
                        href = element.get_attribute("href")
                        href_list.append(href)

                    for href in href_list:
                        sleep(3)
                        driver.get(href)
                        company_name_elements = driver.find_elements(By.XPATH, xpath_element.company_name_and_elements)
                        company_location_elements = driver.find_elements(By.XPATH, xpath_element.company_location)
                        company_name_and_location = [f"{name.text} ({loc.text})" for name, loc in
                                                     zip(company_name_elements, company_location_elements)]

                        business_domain_elements = driver.find_elements(By.XPATH, xpath_element.business_elements)
                        business_domain = [elem.text for elem in business_domain_elements]

                        li_company_name_and_location.extend(company_name_and_location)
                        li_business_domain.extend(business_domain)

                except NoSuchElementException:
                    href_elements = ""
                    li_company_name_and_location = ""
                    li_business_domain = ""

                # Extracting primary skills
                try:
                    driver.get(url + "/details/skills/")
                    li_skills_only = driver.find_elements(By.XPATH, xpath_element.skills_only_elements)
                    li_skills_text = [element.text for element in li_skills_only if element.text.strip() != ""]
                except NoSuchElementException:
                    li_skills_text = []
                li_skills_str = set(li_skills_text).union(found_skills)
                li_skills = ', '.join(list(li_skills_str))

                # Creating a data row for writing to a file
                data_row = [row[0], li_first_name, li_last_name, li_city_id, li_current_location, li_headline,
                            li_alternative_location, li_company_name_and_location, li_skills, li_business_domain,
                            li_positions, li_education, li_certificate,
                            li_languages]

                # Check if any data is present before writing to a file
                if any(data_row[1:]):
                    writer.writerow(data_row)
                    print(f"Profile ID: {row[0]} - Success")
                else:
                    failed = f"Profile ID: {row[0]} - 'position is not defined'"
                    status = "position is not defined"
                    print(failed)
                    with open('failed_scrapped_profiles', 'a', encoding="utf-8", newline='') as csvfile:
                        fieldnames = ['id', "linkedin_url", 'status']  # Specify only the necessary fields
                        wicher = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                        wicher.writerow({'id': id, "linkedin_url": url, 'status': status})

            except TimeoutException:
                print(f"Profile ID: {row[0]} - Failed")
            driver.implicitly_wait(delay)
            continue



