import requests
import csv
import time
from datetime import datetime

# Search terms: focused for immigration-related repos
search_terms = [
    "immigration in:name,description",
    "asylum in:name,description",
    "deportation in:name,description",
    "refugee in:name,description",
    "border aid in:name,description",
    "know-your-rights in:name,description",
    "ICE in:name,description"
]

headers = {'Accept': 'application/vnd.github.v3+json'}
seen_links = set()
results = []

# Query GitHub API for each term
for term in search_terms:
    url = f"https://api.github.com/search/repositories?q={term}&sort=stars&order=desc&per_page=10"
    print(f"Querying: {term}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for item in data.get("items", []):
            link = item["html_url"]
            if link not in seen_links:
                seen_links.add(link)
                results.append({
                    "Name": item["name"],
                    "Source": "GitHub",
                    "Category": "Repo",
                    "Description": item["description"],
                    "Link": link
                })

        time.sleep(2)  # Respect API rate limits

    except Exception as e:
        print(f"Error querying '{term}': {e}")
        continue

# Save to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"immigration_tools_deduped_{timestamp}.csv"

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Source", "Category", "Description", "Link"])
    writer.writeheader()
    for entry in results:
        writer.writerow(entry)

print(f"\nSaved {len(results)} unique projects to {filename}")
