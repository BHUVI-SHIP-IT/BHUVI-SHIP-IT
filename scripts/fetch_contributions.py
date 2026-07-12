import os
import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions():
    username = os.environ.get("GH_PROFILE_USER", "BHUVI-SHIP-IT")
    url = f"https://github.com/users/{username}/contributions"
    
    print(f"Fetching contributions for {username}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to fetch {url} (status {resp.status_code})")
        return
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    contributions = []
    # Find all table cells representing days
    # GitHub uses <td class="ContributionCalendar-day" data-date="..." data-level="...">
    days = soup.find_all('td', {'class': 'ContributionCalendar-day'})
    for day in days:
        date = day.get('data-date')
        level = day.get('data-level')
        if date and level:
            contributions.append({
                "date": date,
                "level": int(level)
            })
            
    # Also grab the "X contributions in the last year" text if possible, but for simplicity let's stick to the grid.
    
    os.makedirs("data", exist_ok=True)
    out_path = "data/contributions.json"
    with open(out_path, "w") as f:
        json.dump(contributions, f, indent=2)
        
    print(f"Saved {len(contributions)} days of contributions to {out_path}")

if __name__ == "__main__":
    fetch_contributions()
