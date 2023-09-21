# linkedin_scraper

This project is intended for parsing profiles on LinkedIn.

Here's how it works:

To get started, we use the data from the file "tsp_profiles.csv" to navigate through the profiles.

Processed profiles are saved in the "scrapped_profiles.csv" file.

Run the following commands to run the scraper: python parsing_profile.py --id ... --login ... --password ... --delay 0.4

In this team:

"parsing_profile.py" is the name of the file from which the launch is made.
"--id" - specifies the initial ID for processing profiles. The ID is taken from the file "tsp_profiles.csv".
"--login" is your login for LinkedIn login.
"--password" is your LinkedIn login password.
"--delay" - sets a delay between profile transitions (by default 0.4 seconds).
This project is designed to work with Python version 3.11.3.
