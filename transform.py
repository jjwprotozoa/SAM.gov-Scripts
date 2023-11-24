import json
import importrequestv3

# Your JSON data (make sure to replace this string with your actual JSON data)
raw_api_response = """
 {
    "totalRecords": 2390,
    "limit": 10,
    "offset": 0,
    "opportunitiesData": [
        {
            "noticeId": "c5712a70b76941f58cca69072a0d31dd",
            "title": "OS42-0050-A3 Serial Synchronous Converter",
            "solicitationNumber": "N6893623Q0157",
            "fullParentPathName": "DEPT OF DEFENSE.DEPT OF THE NAVY.NAVAIR.NAVAIR NAWC WD.NAVAL AIR WARFARE CENTER",
            "fullParentPathCode": "017.1700.NAVAIR.NAVAIR NAWC WD.N68936",
            "postedDate": "2023-05-10",
            "type": "Combined Synopsis/Solicitation",
            "baseType": "Presolicitation",
            "archiveType": "autocustom",
            "archiveDate": "2024-05-21",
            "typeOfSetAsideDescription": null,
            "typeOfSetAside": null,
            "responseDeadLine": "2023-05-22T09:00:00-07:00",
            "naicsCode": "334290",
            "naicsCodes": [
                "334290"
            ],
            "classificationCode": "6125",
            "active": "Yes",
            "award": null,
            "pointOfContact": [
                {
                    "fax": "",
                    "type": "primary",
                    "email": "yvonne.c.stockwell.civ@us.navy.mil",
                    "phone": "7607934069",
                    "title": null,
                    "fullName": "Yvonne Stockwell"
                },
                {
                    "fax": "",
                    "type": "secondary",
                    "email": "faith.l.lagore.civ@us.navy.mil",
                    "phone": "7607933498",
                    "title": null,
                    "fullName": "Faith L LaGore"
                }
            ],
            "description": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=c5712a70b76941f58cca69072a0d31dd",
            "organizationType": "OFFICE",
            "officeAddress": {
                "zipcode": "93555-6018",
                "city": "CHINA LAKE",
                "countryCode": "USA",
                "state": "CA"
            },
            "placeOfPerformance": {},
            "additionalInfoLink": null,
            "uiLink": "https://sam.gov/opp/c5712a70b76941f58cca69072a0d31dd/view",
            "links": [
                {
                    "rel": "self",
                    "href": "https://api.sam.gov/prod/opportunities/v2/search?noticeid=c5712a70b76941f58cca69072a0d31dd&limit=1"
                }
            ],
            "resourceLinks": [
                "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/4ce6747efcd94fed86727c3ef10127d7/download?api_key=null&token="
            ]
        },
        {
            "noticeId": "af225f4ee8b94ee8b3c9692b25ea7d07",
            "title": "ESM ELECTRONICS ASSEMBLY (EEA) SERVICE LIFE EXTENSION PROGRAM (SLEP) PARTS - Amplifiers",
            "solicitationNumber": "N6660423Q0440",
            "fullParentPathName": "DEPT OF DEFENSE.DEPT OF THE NAVY.NAVSEA.NAVSEA WARFARE CENTER.NUWC DIV NEWPORT",
            "fullParentPathCode": "017.1700.NAVSEA.NAVSEA WARFARE CTR.N66604",
            "postedDate": "2023-05-10",
            "type": "Combined Synopsis/Solicitation",
            "baseType": "Combined Synopsis/Solicitation",
            "archiveType": "autocustom",
            "archiveDate": "2023-12-31",
            "typeOfSetAsideDescription": "Total Small Business Set-Aside (FAR 19.5)",
            "typeOfSetAside": "SBA",
            "responseDeadLine": "2023-05-15T14:00:00-04:00",
            "naicsCode": "334511",
            "naicsCodes": [
                "334511"
            ],
            "classificationCode": "5996",
            "active": "Yes",
            "award": null,
            "pointOfContact": [
                {
                    "fax": null,
                    "type": "primary",
                    "email": "elyce.c.hall.civ@us.navy.mil",
                    "phone": "4018324763",
                    "title": null,
                    "fullName": "Elyce Hall"
                },
                {
                    "fax": "",
                    "type": "secondary",
                    "email": "debra.j.dube.civ@us.navy.mil",
                    "phone": "",
                    "title": null,
                    "fullName": "Debra J Dube"
                }
            ],
            "description": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=af225f4ee8b94ee8b3c9692b25ea7d07",
            "organizationType": "OFFICE",
            "officeAddress": {
                "zipcode": "02841-1703",
                "city": "NEWPORT",
                "countryCode": "USA",
                "state": "RI"
            },
            "placeOfPerformance": {
                "city": {
                    "code": "49960",
                    "name": "Newport"
                },
                "state": {
                    "code": "RI",
                    "name": "Rhode Island"
                },
                "zip": "02841",
                "country": {
                    "code": "USA"
                }
            },
            "additionalInfoLink": null,
            "uiLink": "https://sam.gov/opp/af225f4ee8b94ee8b3c9692b25ea7d07/view",
            "links": [
                {
                    "rel": "self",
                    "href": "https://api.sam.gov/prod/opportunities/v2/search?noticeid=af225f4ee8b94ee8b3c9692b25ea7d07&limit=1"
                }
            ],
            "resourceLinks": [
                "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/f272d7609a1d40b8a5162b562c8bef71/download?api_key=null&token="
            ]
        }
    ]
}

"""

def extract_nested_data(nested_data):
    """
    Recursively extract data from nested dictionaries and lists.
    """
    if isinstance(nested_data, dict):
        return {k: extract_nested_data(v) for k, v in nested_data.items()}
    elif isinstance(nested_data, list):
        return [extract_nested_data(item) for item in nested_data]
    else:
        return nested_data

def process_opportunities(api_data):
    
    opportunities = api_data["opportunitiesData"]
    
    extracted_opps = []
    
    # Loop through each opportunity
    for opportunity in opportunities:
      
        # Extract nested data 
        extracted_opp = extract_nested_data(opportunity)
        
        # Further processing 
        format_datetime(extracted_opp)
        format_contacts(extracted_opp)
        
        extracted_opps.append(extracted_opp)
        
    return extracted_opps

def extract_nested_data(nested_data):

    # Recursive extraction logic
    pass 

def format_datetime(opp):

    # Format date/time logic  
    pass

def format_contacts(opp):
  
    poc = opp["pointOfContact"] 
    primary, secondary = importrequestv3.format_poc(poc)
    
    opp["primaryContact"] = primary 
    opp["secondaryContact"] = secondary

# Main execution block
if __name__ == "__main__":
    try:
        # Convert the JSON string into a Python dictionary
        data = json.loads(raw_api_response)

        # Process opportunities and extract all information
        transformed_data = process_opportunities(data)

        # Print the transformed data
        print(json.dumps(transformed_data, indent=4))

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        if __name__ == "__main__":