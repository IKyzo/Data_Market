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

        # Selectors for both featured and regular jobs
        job_elements = soup.find_all('div', style='float:left;width:350px; border:solid 2px #e2e2e2;-moz-border-radius:4px;-webkit-border-radius:4px; min-height:220px;margin:5px; padding:5px;')

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
                job_title_element = job.find('h1').find('a')
                job_description_element = job.find('div', style='line-height:18px;font-size:12px; font-family:Verdana, Geneva, sans-serif')
                company_and_title_element = job_title_element.text.strip().split('recrute', 1)

                # Extract company name and job title
                company_name = company_and_title_element[0].strip()
                job_title = company_and_title_element[1].strip() if len(company_and_title_element) > 1 else "Job Title not found"

                # Other extraction remains the same
                job_location_element = job.find('a', href=lambda value: value and 'category/pays/' in value)
                tag = "featured" if "listing-item__featured" in job.get('class', []) else "available"

                # Append data to lists
                job_titles.append(job_title)
                job_descriptions.append(job_description_element.text.strip() if job_description_element else "Description not found")
                company_names.append(company_name)
                job_locations.append(job_location_element.text.strip() if job_location_element else "Location not found")
                tags.append(tag)

            # Check if lengths of arrays are the same
            if len(set(map(len, [job_titles, job_descriptions, company_names, job_locations, tags]))) > 1:
                print("Error: Lengths of arrays are not the same.")
                return None

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
base_url = "https://www.tunisietravail.net/category/pays/tunisie/sousse/"

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
