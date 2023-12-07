import requests


def get_article_data_from_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["message"]
        # Extract relevant fields from data
        title = data.get("title", [""])[0]  # Assuming the first title is the main one
        journal_name = data.get("container-title", [""])[0]
        # Add other fields as needed
        return {
            "title": title,
            "journal_name": journal_name,
            # Add other fields
        }
    else:
        return None
