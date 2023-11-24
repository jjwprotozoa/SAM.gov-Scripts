# transform.py

import json

test_data = '''
{
  "opportunities": [
    {
      "id": "abc123",
      "title": "Example Opportunity"
    },
    {
      "id": "def456",  
      "title": "Second Example"
    }
  ]
}
'''

def process_data(data):
  opportunities = data['opportunities']
  
  for opp in opportunities:
    print(opp['title'])
    
if __name__ == '__main__':

  try:
    data = json.loads(test_data)  
    process_data(data)
  
  except Exception as e:
    print('Error:', e)