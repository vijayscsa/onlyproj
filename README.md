source venv/bin/activate
python -c "
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('PAGERDUTY_USER_API_KEY', 'NOT SET')
api_host = os.getenv('PAGERDUTY_API_HOST', 'https://api.pagerduty.com')

print(f'API Key: {api_key[:10]}...' if len(api_key) > 10 else f'API Key: {api_key}')
print(f'API Host: {api_host}')

try:
    response = httpx.get(
        f'{api_host}/services',
        headers={
            'Authorization': f'Token token={api_key}',
            'Content-Type': 'application/json'
        },
        params={'limit': 1},
        timeout=10
    )
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ PagerDuty connection working!')
    else:
        print(f'Response: {response.text[:300]}')
except Exception as e:
    print(f'Error: {e}')
"
