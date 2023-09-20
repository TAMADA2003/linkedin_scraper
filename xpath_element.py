name_element = "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']"

location_element = "//span[@class='text-body-small inline t-black--light break-words']"

alternative_location_element = "//section[contains(., 'Experience')]//span[@class='t-14 t-normal t-black--light' and not(contains(., 'yrs')) and not(contains(., 'yr')) and not(contains(.,'mos'))]"

headline_element = "//div[@class='text-body-medium break-words']"

position_element = "//section[contains(., 'Experience')]//div[@class='display-flex flex-column full-width align-self-center']//div[@class='display-flex flex-wrap align-items-center full-height']"

position_text_element = "(//section[contains(., 'Experience')]//div[@class='display-flex flex-column full-width align-self-center']//div[@class='display-flex flex-wrap align-items-center full-height']//span[@aria-hidden='true'])"

position_time_element = "(//section[contains(., 'Experience')]//span[@class='t-14 t-normal t-black--light' and (contains(., 'yrs') or contains(., 'yr')) or contains(.,'mos')]//span[@aria-hidden='true'])"

education_time_elements = "//section[contains(.,'Education')]//div[@class='display-flex flex-column full-width align-self-center']//span[@class='t-14 t-normal t-black--light']//span[@aria-hidden='true']"

education_text_elements = "//section[contains(.,'Education')]//div[@class='display-flex flex-column full-width align-self-center']//div[@class='display-flex flex-wrap align-items-center full-height']//span[@aria-hidden='true']"

certificate_text_elements = "//section[contains(.,'Licenses & certifications')]//div[@class='pvs-list__outer-container']//div[@class='display-flex flex-wrap align-items-center full-height']//span[@aria-hidden='true']"

certificate_time_elements = "//section[contains(.,'Licenses & certifications')]//div[@class='pvs-list__outer-container']//span[@class='t-14 t-normal t-black--light']//span[@aria-hidden='true'and (contains(.,'Issued'))]"

languages_text_elements = "//section[contains(.,'Languages')]//div[@class='pvs-list__outer-container']//div[@class='display-flex flex-wrap align-items-center full-height']//span[@aria-hidden='true']"

languages_level_elements = "//section[contains(.,'Languages')]//div[@class='pvs-list__outer-container']//span[@class='t-14 t-normal t-black--light']//span[@aria-hidden='true']"

skills_subsequent_elements = "//section[contains(.,'About')]//div[@class='display-flex ph5 pv3']//span[@aria-hidden='true']"

skills_subsequent_2_elements = "//section[contains(.,'Experience')]//div[@class='pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center']//span[@aria-hidden='true']"

href_elements = "//a[@data-field='experience_company_logo' and contains(@href, '/company')]"

company_name_and_elements = "//div[@class='block mt2']//span[@dir='ltr']"

company_location = "//div[@class='block mt2']//div[@class='inline-block']//div[@class='org-top-card-summary-info-list__info-item'][1]"

business_elements = "//div[@class='org-top-card-summary-info-list']//div[@class='org-top-card-summary-info-list__info-item'][1 or 2]"

skills_only_elements = "//section[contains(.,'Skills')]//div[@class='pvs-list__container']//span[@class='mr1 hoverable-link-text t-bold']//span[@aria-hidden='true']"