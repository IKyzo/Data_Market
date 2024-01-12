import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Function to scrape data from a specific page
def scrape_page(url):
    response = requests.get(url)

    # Request was successful code: 200
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Selectors for job elements
        job_elements = soup.find_all('div', class_='col-lg-5 col-md-5 col-sm-5 col-xs-12 job-title')

        # Check if any job elements were found
        if job_elements:
            print(f"Found {len(job_elements)} job elements on {url}.")

            # Initialize lists to store data
            job_titles = []
            job_descriptions = []
            company_names = []
            job_locations = []
            tags = []  # New column for tags

            # Iterating through elements
            for job in job_elements:
                job_title_element = job.find('h5').find('a')
                job_description_element = job.find('div', class_='search-description')
                company_name_element = job.find('p', class_='job-recruiter').find('b').find('a')

                # Extract location
                location_element = job.find('p', text='Région de :')
                location = location_element.find_next('p').text.strip() if location_element else "Location not found"

                # Extract tags
                tags_element = job.find('div', class_='job-tags')
                tags_list = [tag.text.strip() for tag in tags_element.find_all('div', class_='badge')] if tags_element else []

                # Extract data and append to lists
                job_titles.append(job_title_element.text.strip() if job_title_element else "Title not found")
                job_descriptions.append(job_description_element.text.strip() if job_description_element else "Description not found")
                company_names.append(company_name_element.text.strip() if company_name_element else "Company not found")
                job_locations.append(location)
                tags.append(tags_list)

            # Create a DataFrame
            data = {'Job Title': job_titles, 'Description': job_descriptions, 'Company': company_names, 'Location': job_locations, 'Tags': tags}
            df = pd.DataFrame(data)

            return df

        else:
            print(f"No job elements found on {url}.")

    else:
        print(f"Failed to retrieve the page {url}. Status Code: {response.status_code}")
        return None

# Main code to iterate through pages
base_url = "https://www.emploitunisie.com/recherche-jobs-tunisie?f%5B0%5D=im_field_offre_region%3A955&page=1"

# Uncomment the line below and set the range of pages you want to scrape
# start_page = 1
# end_page = 1  # Change this to the desired end page

# Initialize an empty DataFrame to store the results
final_df = pd.DataFrame()

# Uncomment the loop below if you want to scrape multiple pages
# for page_number in range(start_page, end_page + 1):
#     page_url = f"{base_url}{page_number}"
page_df = scrape_page(base_url)

if page_df is not None:
    final_df = pd.concat([final_df, page_df], ignore_index=True)

    # Display the final DataFrame
    print(final_df)

    # Generate a new filename based on the current date and time
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f'job_data_all_pages_{current_datetime}.xlsx'

    # Save the final DataFrame to an Excel file
    final_df.to_excel(new_filename, index=False)
