import requests, json
from transform import process_opportunities 
from opportunity_gui import get_filters, display_opps
import csv

# Set-Aside Types for selection
set_aside_types = {
    "SBA": "Total Small Business Set-Aside (FAR 19.5)",
    "SBP": "Partial Small Business Set-Aside (FAR 19.5)",
    # ... (include all other types here)
}

# Timezone mapping for US states
state_timezones = {
    'AL': 'America/Chicago', 'AK': 'America/Anchorage', 'AZ': 'America/Phoenix',
    'AR': 'America/Chicago', 'CA': 'America/Los_Angeles', 'CO': 'America/Denver',
    'CT': 'America/New_York', 'DE': 'America/New_York', 'FL': 'America/New_York',
    'GA': 'America/New_York', 'HI': 'Pacific/Honolulu', 'ID': 'America/Denver',
    'IL': 'America/Chicago', 'IN': 'America/New_York', 'IA': 'America/Chicago',
    'KS': 'America/Chicago', 'KY': 'America/New_York', 'LA': 'America/Chicago',
    'ME': 'America/New_York', 'MD': 'America/New_York', 'MA': 'America/New_York',
    'MI': 'America/New_York', 'MN': 'America/Chicago', 'MS': 'America/Chicago',
    'MO': 'America/Chicago', 'MT': 'America/Denver', 'NE': 'America/Chicago',
    'NV': 'America/Los_Angeles', 'NH': 'America/New_York', 'NJ': 'America/New_York',
    'NM': 'America/Denver', 'NY': 'America/New_York', 'NC': 'America/New_York',
    'ND': 'America/Chicago', 'OH': 'America/New_York', 'OK': 'America/Chicago',
    'OR': 'America/Los_Angeles', 'PA': 'America/New_York', 'RI': 'America/New_York',
    'SC': 'America/New_York', 'SD': 'America/Chicago', 'TN': 'America/Chicago',
    'TX': 'America/Chicago', 'UT': 'America/Denver', 'VT': 'America/New_York',
    'VA': 'America/New_York', 'WA': 'America/Los_Angeles', 'WV': 'America/New_York',
    'WI': 'America/Chicago', 'WY': 'America/Denver'
}

# Function to get user input
def get_user_input():
    api_key = input("Enter your API key: ")
    start_date = input("Enter start date (MM/DD/YYYY): ")
    end_date = input("Enter end date (MM/DD/YYYY): ")
    limit = input("Enter the number of records to fetch: ")
    include_awards = input("Include awards? (yes/no): ").lower() == 'yes'
    keyword = input("Enter a keyword for filtering (leave blank if not needed): ")

    print("Available Set-Aside Types:")
    for code, description in set_aside_types.items():
        print(f"{code} - {description}")

    set_aside_filter = input("Enter Set-Aside code for filtering (leave blank if not needed): ").upper()
    return api_key, start_date, end_date, limit, include_awards, keyword, set_aside_filter

# Function to fetch data from the API
def fetch_data(api_key, start_date, end_date, limit):
    api_url = f"https://api.sam.gov/opportunities/v2/search?limit={limit}&api_key={api_key}&postedFrom={start_date}&postedTo={end_date}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print("Error details:", response.text)
        return None

# Function to format the point of contact
def format_poc(poc_data):
    primary_contact = "Not available"
    secondary_contact = "Not available"

    for contact in poc_data:
        contact_str = f"{contact['fullName']}"
        if contact['email']:
            contact_str += f" (Email: {contact['email']})"
        if contact['phone']:
            contact_str += f" (Phone: {contact['phone']})"

        if contact['type'].lower() == 'primary':
            primary_contact = contact_str
        elif contact['type'].lower() == 'secondary':
            secondary_contact = contact_str

    return primary_contact, secondary_contact

# Function to format place of performance
def format_place_of_performance(place_data):
    if not place_data:
        return "Not available"
    city = place_data.get('city', {}).get('name', 'Not available')
    state = place_data.get('state', {}).get('name', 'Not available')
    zip_code = place_data.get('zip', 'Not available')
    country = place_data.get('country', {}).get('name', 'Not available')

    formatted_place = f"{city}, {state}, {zip_code}, {country}"
    return formatted_place

# Function to filter and format data
def filter_data(data, include_awards, keyword, selected_set_aside):
    filtered_data = []
    for opportunity in data.get("opportunitiesData", []):
        # ... (Existing code to filter and format data)

        primary_contact, secondary_contact = format_poc(opportunity.get('pointOfContact', []))
        opportunity['primaryContact'] = primary_contact
        opportunity['secondaryContact'] = secondary_contact

        opportunity['placeOfPerformance'] = format_place_of_performance(opportunity.get('placeOfPerformance'))

# Function to format the address
def format_address(address):
    if not address:
        return "Not available"
    formatted_address = ', '.join(filter(None, [
        address.get('streetAddress', ''),
        address.get('city', ''),
        address.get('state', ''),
        address.get('zipcode', ''),
        address.get('countryCode', '')
    ]))
    return formatted_address

# Function to format and split datetime with inferred timezone
def format_split_datetime_with_inferred_timezone(dt_str, state_code):
    if not dt_str:
        return "Not available", "Not available", "Not available"

    # Infer timezone from state
    tz_str = state_timezones.get(state_code, 'UTC')  # Default to UTC
    tz = timezone(tz_str)
    dt = parser.parse(dt_str).astimezone(tz)

    date = dt.strftime("%Y-%m-%d")
    time = dt.strftime("%H:%M:%S")
    timezone_name = dt.tzname()
    return date, time, timezone_name

def format_award_data(award):
    if not award:
        return "Not available"
    formatted_award = f"Date: {award.get('date', 'Not available')}, " \
                      f"Number: {award.get('number', 'Not available')}, " \
                      f"Amount: {award.get('amount', 'Not available')}, " \
                      f"Awardee: {award.get('awardee', {}).get('name', 'Not available')}"
    return formatted_award

# Function to filter and format data
def filter_data(data, include_awards, keyword, selected_set_aside):
    filtered_data = []
    for opportunity in data.get("opportunitiesData", []):
        opportunity_type = opportunity.get("type", "").lower()
        base_type = opportunity.get("baseType", "").lower()

        # Exclude presolicitations
        if 'presolicitation' in opportunity_type or 'presolicitation' in base_type:
            continue

        if include_awards or "solicitation" in opportunity_type:
            if keyword and keyword.lower() not in opportunity.get("title", "").lower():
                continue
            if selected_set_aside and opportunity.get("typeOfSetAside", "") != selected_set_aside:
                continue

        primary_contact, secondary_contact = format_poc(opportunity.get('pointOfContact', []))
        opportunity['primaryContact'] = primary_contact
        opportunity['secondaryContact'] = secondary_contact
        del opportunity['pointOfContact']  # Remove original pointOfContact field

        opportunity['placeOfPerformance'] = format_place_of_performance(opportunity.get('placeOfPerformance'))

        opportunity['award'] = format_award_data(opportunity.get('award'))

        office_address = opportunity.get('officeAddress', {}) or {}
        opportunity['officeAddress'] = format_address(office_address)

        # Infer timezone from officeAddress state
        state_code = office_address.get('state', '')
        posted_date, posted_time, posted_tz = format_split_datetime_with_inferred_timezone(opportunity.get('postedDate', ''), state_code)
        opportunity['postedDate'] = posted_date
        opportunity['postedTime'] = posted_time
        opportunity['postedTZ'] = posted_tz

        deadline_date, deadline_time, deadline_tz = format_split_datetime_with_inferred_timezone(opportunity.get('responseDeadLine', ''), state_code)
        opportunity['responseDeadLineDate'] = deadline_date
        opportunity['responseDeadLineTime'] = deadline_time
        opportunity['responseDeadLineTZ'] = deadline_tz

        filtered_data.append(opportunity)
    return filtered_data

# Function to save data to a CSV file
def save_to_csv(opportunities, filename):
    if not opportunities:
        print("No opportunities to save.")
        return

    # Get filters from GUI   
    filters = opportunity_gui.get_filters()
    
    # Fetch and transform
    data = fetch_data(api_key, start_date, end_date, limit) 
    opportunities = transform.process(data)

    # Filter  
    filtered_opps = filter_data(opportunities, filters)

    # Output results  
    opportunity_gui.display_opps(filtered_opps)
    save_to_csv(filtered_opps, "output.csv")

    # Check if the file is open
    file_open = True
    while file_open:
        response = input(f"Please ensure that the file '{filename}' is closed. Type 'yes' when ready: ").lower()
        if response == 'yes':
            file_open = False

    try:
        keys = opportunities[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, quoting=csv.QUOTE_NONNUMERIC)
            dict_writer.writeheader()
            dict_writer.writerows(opportunities)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Main execution
api_key, start_date, end_date, limit, include_awards, keyword, selected_set_aside = get_user_input()
data = fetch_data(api_key, start_date, end_date, limit)
if data:
    print("Raw API Response:")
    print(json.dumps(data, indent=4))

    num_results = len(data.get("opportunitiesData", []))
    print(f"Number of search results found: {num_results}")

    filtered_opportunities = filter_data(data, include_awards, keyword, selected_set_aside)
    if filtered_opportunities:
        print("Filtered Opportunities:")
        print(json.dumps(filtered_opportunities, indent=4))
        save_to_csv(filtered_opportunities, "opportunities.csv")
        print("Data saved to opportunities.csv")
    else:
        print("No matching opportunities found.")
else:
    print("No data received from API.")

# Helper functions

def main():

    filters = get_filters()
        
    data = fetch_data()  

    opportunities = process_opportunities(data)

    filtered_opps = filter_opps(opportunities, filters)

    display_opps(filtered_opps)
    
    save_to_csv(filtered_opps, "output.csv")


if __name__ == "__main__":
    main()