import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def main():
    # Replace with your actual GitHub username
    username = 'PedroRouge'
    url = f'https://github.com/users/{username}/contributions'
    
    print(f'Fetching contributions for {username} from {url}...')
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f'Error: Failed to fetch contributions (status code {response.status_code})')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    days = []
    
    # Parse contribution cells from GitHub's calendar HTML
    for rect in soup.find_all('td', class_='ContributionCalendar-day'):
        date = rect.get('data-date')
        level = rect.get('data-level')
        count_text = rect.get('id') # or parse text
        
        # Determine count based on data-level or aria-label
        aria = rect.get('aria-label', '')
        count = 0
        if 'no contribution' not in aria.lower():
            parts = aria.split(' ')
            if parts and parts[0].isdigit():
                count = int(parts[0])
                
        if date:
            days.append({
                'date': date,
                'count': count,
                'level': int(level) if level else 0
            })

    os.makedirs('data', exist_ok=True)
    output_path = 'data/contributions.json'
    
    data = {
        'fetched_at': datetime.utcnow().isoformat(),
        'days': days
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f'Successfully saved {len(days)} days of contributions to {output_path}')

if __name__ == '__main__':
    main()
