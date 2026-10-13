import os
import re
import json
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

def fetch_via_graphql(username, token):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "PedroRouge-Profile-Updater"
    }
    
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"login": username}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code != 200:
        print(f"GraphQL request failed: HTTP {response.status_code}")
        return None
        
    res_data = response.json()
    if "errors" in res_data:
        print("GraphQL returned errors:", res_data["errors"])
        return None
        
    try:
        calendar = res_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total = calendar["totalContributions"]
        days = []
        
        # Level mapping from GitHub GraphQL strings to integers 0-4
        level_map = {
            "NONE": 0,
            "FIRST_QUARTILE": 1,
            "SECOND_QUARTILE": 2,
            "THIRD_QUARTILE": 3,
            "FOURTH_QUARTILE": 4
        }
        
        for week in calendar["weeks"]:
            for d in week["contributionDays"]:
                days.append({
                    "date": d["date"],
                    "count": d["contributionCount"],
                    "level": level_map.get(d["contributionLevel"], 0)
                })
                
        days.sort(key=lambda x: x["date"])
        print(f"Successfully fetched {len(days)} days ({total} contributions) via GitHub GraphQL API!")
        return {"total": total, "days": days}
    except Exception as e:
        print("Error parsing GraphQL response:", e)
        return None

def fetch_via_scraping(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to scrape contributions: HTTP {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    tooltips = {tt.get("for"): tt.text.strip() for tt in soup.find_all("tool-tip") if tt.get("for")}

    days = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date_str = td.get("data-date")
        if not date_str:
            continue
        level = int(td.get("data-level", 0))
        cid = td.get("id")
        tt_text = tooltips.get(cid, "")
        
        count = 0
        m = re.search(r"(\d+)\s+contribution", tt_text)
        if m:
            count = int(m.group(1))
        elif level > 0:
            count = level
            
        days.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    days.sort(key=lambda x: x["date"])
    total = sum(d["count"] for d in days)
    print(f"Successfully fetched {len(days)} days ({total} contributions) via Web Scraping fallback.")
    return {"total": total, "days": days}

def main():
    username = "PedroRouge"
    token = os.environ.get("GITHUB_TOKEN")
    
    result = None
    if token:
        print(f"GITHUB_TOKEN found. Querying GitHub GraphQL API for {username}...")
        result = fetch_via_graphql(username, token)
        
    if not result:
        print(f"Querying GitHub web interface for {username}...")
        result = fetch_via_scraping(username)

    if not result or not result["days"]:
        print("Error: Could not retrieve contributions data.")
        return

    os.makedirs("data", exist_ok=True)
    output_path = "data/contributions.json"
    
    data = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": result["total"],
        "days": result["days"]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully saved contributions to {output_path}")

if __name__ == "__main__":
    main()
