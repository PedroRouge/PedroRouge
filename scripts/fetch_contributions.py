import os
import re
import json
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

def main():
    username = 'PedroRouge'
    url = f'https://github.com/users/{username}/contributions'
    
    print(f'Fetching real live contributions for {username} from {url}...')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f'Error: Failed to fetch contributions (status code {response.status_code})')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Map tooltip texts by element id
    tooltips = {tt.get('for'): tt.text.strip() for tt in soup.find_all('tool-tip') if tt.get('for')}

    days = []
    # Parse contribution cells from GitHub's calendar HTML
    for td in soup.find_all('td', class_='ContributionCalendar-day'):
        date_str = td.get('data-date')
        if not date_str:
            continue
            
        level = int(td.get('data-level', 0))
        cid = td.get('id')
        tt_text = tooltips.get(cid, '')
        
        count = 0
        m = re.search(r'(\d+)\s+contribution', tt_text)
        if m:
            count = int(m.group(1))
        elif level > 0:
            count = level
            
        days.append({
            'date': date_str,
            'count': count,
            'level': level
        })

    days.sort(key=lambda x: x['date'])

    os.makedirs('data', exist_ok=True)
    output_path = 'data/contributions.json'
    
    total = sum(d['count'] for d in days)
    data = {
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'total_contributions': total,
        'days': days
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f'Successfully saved {len(days)} days ({total} real contributions) to {output_path}')

if __name__ == '__main__':
    main()
