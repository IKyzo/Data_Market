import requests

url = "https://www.linkedin.com/jobs/job-jobs-enfidha?src_gapi=6282&position=1&pageNum=0"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    print("We Gucci ")
    # Process the HTML content as needed
else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")
