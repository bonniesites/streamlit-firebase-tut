import json
import csv

# Your JSON data
json_data = '''
{
    "count": 879,
    "entities": [
        {
            "uuid": "0e8aeaff-bbd3-cebc-7b8d-dedb6c239b11",
            "properties": {
                "company_type": "for_profit",
                "location_group_identifiers": [
                    {
                        "permalink": "greater-minneapolis-saint-paul-area",
                        "uuid": "8d94f1af-91f2-413a-a287-38de0f7bfa92",
                        "location_type": "group",
                        "entity_def_id": "location",
                        "value": "Greater Minneapolis-Saint Paul Area"
                    },
                    {
                        "permalink": "great-lakes-north-america",
                        "uuid": "645645b9-0033-4c72-aa83-2ae8c6062d55",
                        "location_type": "group",
                        "entity_def_id": "location",
                        "value": "Great Lakes"
                    },
                    {
                        "permalink": "midwestern-united-states",
                        "uuid": "4bf64c61-8537-435a-9748-c567a59483e4",
                        "location_type": "group",
                        "entity_def_id": "location",
                        "value": "Midwestern US"
                    }
                ],
                "num_investments_funding_rounds": 9,
                "founded_on": {
                    "precision": "year",
                    "value": "1902-01-01"
                },
                "website": {
                    "value": "https://www.3m.com"
                },
                "phone_number": "+1 651 733 1110",
                "identifier": {
                    "permalink": "3m",
                    "image_id": "v1397204757/ed6f4c213bec81dd2615323c6527d489.gif",
                    "uuid": "0e8aeaff-bbd3-cebc-7b8d-dedb6c239b11",
                    "entity_def_id": "organization",
                    "value": "3M"
                },
                "ipo_status": "public",
                "description": "3M operates as a diversified technology company, manufacturing products, including adhesives, abrasives, laminates, passive fire protection, dental and orthodontic products, electronic materials, medical products, car-care products, electronic circuits, and optical films. It operates in the industrial and transportation; health care; safety, security, and protection services; consumer and office; display and graphics; and electro and communications businesses. Its industrial and transportation business serves a range of markets, such as appliance, paper and packaging, food and beverage, electronics, automotive original equipment manufacturer, and automotive aftermarket.",
                "linkedin": {
                    "value": "http://www.linkedin.com/company/3m"
                },
                "went_public_on": "1978-01-13",
                "short_description": "3M operates as a diversified technology company.",
                "stock_exchange_symbol": "nyse",
                "revenue_range": "r_01000000",
                "num_sub_organizations": 16,
                "last_key_employee_change_date": "2023-08-22",
                "stock_symbol": {
                    "permalink": "3m-ipo--e0c82f24",
                    "image_id": "v1397204757/ed6f4c213bec81dd2615323c6527d489.gif",
                    "uuid": "e0c82f24-4d09-59ca-bd45-d311ef61f83e",
                    "entity_def_id": "ipo",
                    "value": "MMM"
                },
                "num_acquisitions": 76,
                "operating_status": "active",
                "last_layoff_date": "2023-06-15",
                "rank_org": 12339,
                "num_employees_enum": "c_10001_max",
                "num_contacts": 9904,
                "job_posting_link_source": "jobbio",
                "categories": [
                    {
                        "entity_def_id": "category",
                        "permalink": "automotive",
                        "uuid": "bb2ad65f-1009-db81-c6f6-83dbcfd64870",
                        "value": "Automotive"
                    },
                    {
                        "entity_def_id": "category",
                        "permalink": "consulting",
                        "uuid": "b9bd65b9-20bf-45cc-207d-b70ac35d5bf4",
                        "value": "Consulting"
                    },
                    {
                        "entity_def_id": "category",
                        "permalink": "electronics",
                        "uuid": "e173f255-3db1-9d02-74cb-f58a1f45b483",
                        "value": "Electronics"
                    },
                    {
                        "entity_def_id": "category",
                        "permalink": "enterprise-software",
                        "uuid": "d38b3f26-abc4-6f7b-b29d-b952021a1b14",
                        "value": "Enterprise Software"
                    },
                    {
                        "entity_def_id": "category",
                        "permalink": "manufacturing",
                        "uuid": "e811671c-168d-1fd2-36e5-df4e08a09f7c",
                        "value": "Manufacturing"
                    }
                ],
                "location_identifiers": [
                    {
                        "permalink": "saint-paul-minnesota",
                        "uuid": "f22a93cd-c7ad-41f3-024d-743436345095",
                        "location_type": "city",
                        "entity_def_id": "location",
                        "value": "Saint Paul"
                    },
                    {
                        "permalink": "minnesota-united-states",
                        "uuid": "2c75f4b5-8c06-f0cc-4a6d-d780e2b56365",
                        "location_type": "region",
                        "entity_def_id": "location",
                        "value": "Minnesota"
                    },
                    {
                        "permalink": "united-states",
                        "uuid": "f110fca2-1055-99f6-996d-011c198b3928",
                        "location_type": "country",
                        "entity_def_id": "location",
                        "value": "United States"
                    },
                    {
                        "permalink": "north-america",
                        "uuid": "b25caef9-a1b8-3a5d-6232-93b2dfb6a1d1",
                        "location_type": "continent",
                        "entity_def_id": "location",
                        "value": "North America"
                    }
                ],
                "num_event_appearances": 51,
                "twitter": {
                    "value": "https://twitter.com/3M"
                },
                "acquisition_announced_on": {
                    "precision": "day",
                    "value": "2017-06-01"
                },
                "num_exits": 2,
                "rank_org_company": 12304,
                "funding_stage": "m_and_a"
            }
        },
        {
            "uuid": "1755c9e9-c17f-6f23-f6b4-0ffe6c7da3e9",
            "properties": {
                "company_type": "for_profit",
                "location_group_identifiers": [
                    {
                        "permalink": "dallas-fort-worth-metroplex",
                        "uuid": "da8a3958-6314-4c85-b614-f05c9efedc38",
                        "location_type": "group",
                        "entity_def_id": "location",
                        "value": "Dallas/Fort Worth Metroplex"
                    },
                    {
                        "permalink": "southern-united-states",
                        "uuid": "090db99d-13e7-455a-a0e4-95cd21211c92",
                        "location_type": "group",
                        "entity_def_id": "location",
                        "value": "Southern US"
                    }
                ],
                "num_investments_funding_rounds": 4,
                "founded_on": {
                    "precision": "year",
                    "value": "1927-01-01"
                },
                "website": {
                    "value": "http://www.7-eleven.com"
                },
                "phone_number": "4018497190",
                "identifier": {
                    "permalink": "7-eleven-inc",
                    "image_id": "q8smgwpwvcjs5ky6xj0q",
                    "uuid": "1755c9e9-c17f-6f23-f6b4-0ffe6c7da3e9",
                    "entity_def_id": "organization",
                    "value": "7-Eleven"
                },
                "ipo_status": "public",
                "description": "7-Eleven is part of an international chain of convenience stores. 7-Eleven, primarily operating as a franchise, is the world's largest operator, franchisor, and licensor of convenience stores with more than 50,000 outlets. This number surpassed the previous record-holder, McDonald's Corporation, in 2007, by approximately 1,000 retail stores. 7-Eleven branded stores under parent company Seven & I Holdings Co. The stores are located in 16 countries with its largest markets being Japan (15,000), the United States (8,200), Thailand (6,800), Indonesia, Canada, the Philippines, Hong Kong, Taiwan, Malaysia, and Singapore.",
                "ipqwery_num_trademark_registered": 295,
                "ipqwery_num_patent_granted": 108,
                "linkedin": {
                    "value": "https://www.linkedin.com/company/7-eleven/"
                },
                "went_public_on": "1998-02-04",
                "short_description": "7-Eleven is a convenience retailer store with retails of food and beverage.",
                "stock_exchange_symbol": "pse",
                "revenue_range": "r_01000000",
                "stock_symbol": {
                    "permalink": "7-eleven-inc-ipo--9ab72fcf",
                    "image_id": "q8smgwpwvcjs5ky6xj0q",
                    "uuid": "9ab72fcf-5c90-4ed0-a89c-9b744751881c",
                    "entity_def_id": "ipo",
                    "value": "SEVN"
                },
                "num_acquisitions": 4,
                "operating_status": "active",
                "last_layoff_date": "2022-07-21",
                "rank_org": 3971,
                "num_employees_enum": "c_10001_max",
                "num_contacts": 4235,
                "num_funding_rounds": 1,
                "job_posting_link_source": "jobbio",
                "categories": [
                    {
                        "entity_def_id": "category",
                        "permalink": "food-and-beverage",
                        "uuid": "14364faa-63f9-0d45-7b6a-7378113364a2",
                        "value": "Food and Beverage"
                    },
                    {
                        "entity_def_id": "category",
                        "permalink": "retail",
                        "uuid": "b65acba5-b299-3990-6390-8be3e3833a07",
                        "value": "Retail"
                    }
                ],
                "location_identifiers": [
                    {
                        "permalink": "irving-texas",
                        "uuid": "d248f640-a8aa-63e7-f70c-eb5828a27d7f",
                        "location_type": "city",
                        "entity_def_id": "location",
                        "value": "Irving"
                    },
                    {
                        "permalink": "texas-united-states",
                        "uuid": "54e9e76a-1847-d137-00a7-ed1aab624b78",
                        "location_type": "region",
                        "entity_def_id": "location",
                        "value": "Texas"
                    },
                    {
                        "permalink": "united-states",
                        "uuid": "f110fca2-1055-99f6-996d-011c198b3928",
                        "location_type": "country",
                        "entity_def_id": "location",
                        "value": "United States"
                    },
                    {
                        "permalink": "north-america",
                        "uuid": "b25caef9-a1b8-3a5d-6232-93b2dfb6a1d1",
                        "location_type": "continent",
                        "entity_def_id": "location",
                        "value": "North America"
                    }
                ],
                "num_event_appearances": 1,
                "twitter": {
                    "value": "http://twitter.com/7eleven"
                },
                "last_equity_funding_total": {
                    "value_usd": 3000000,
                    "currency": "USD",
                    "value": 3000000
                }
            }
        }
    ]
}
'''

# Load JSON data
data = json.loads(json_data)

# Extract entities
entities = data.get("entities", [])

# Define the CSV file name
csv_file = "entities.csv"

# Define the CSV header
csv_header = [
    "uuid", "company_type", "founded_on", "website", "phone_number", "identifier",
    "ipo_status", "description", "linkedin", "went_public_on", "short_description",
    "stock_exchange_symbol", "revenue_range", "num_sub_organizations",
    "last_key_employee_change_date", "stock_symbol", "num_acquisitions",
    "operating_status", "last_layoff_date", "rank_org", "num_employees_enum",
    "num_contacts", "job_posting_link_source", "num_funding_rounds", "categories",
    "location_identifiers", "num_event_appearances", "twitter",
    "acquisition_announced_on", "num_exits", "rank_org_company", "funding_stage"
]

# Open the CSV file for writing
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=csv_header)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data for each entity
    for entity in entities:
        properties = entity.get("properties", {})
        row = {
            "uuid": entity.get("uuid", ""),
            "company_type": properties.get("company_type", ""),
            "founded_on": properties.get("founded_on", {}).get("value", ""),
            "website": properties.get("website", {}).get("value", ""),
            "phone_number": properties.get("phone_number", ""),
            "identifier": properties.get("identifier", {}).get("value", ""),
            "ipo_status": properties.get("ipo_status", ""),
            "description": properties.get("description", ""),
            "linkedin": properties.get("linkedin", {}).get("value", ""),
            "went_public_on": properties.get("went_public_on", ""),
            "short_description": properties.get("short_description", ""),
            "stock_exchange_symbol": properties.get("stock_exchange_symbol", ""),
            "revenue_range": properties.get("revenue_range", ""),
            "num_sub_organizations": properties.get("num_sub_organizations", ""),
            "last_key_employee_change_date": properties.get("last_key_employee_change_date", ""),
            "stock_symbol": properties.get("stock_symbol", {}).get("value", ""),
            "num_acquisitions": properties.get("num_acquisitions", ""),
            "operating_status": properties.get("operating_status", ""),
            "last_layoff_date": properties.get("last_layoff_date", ""),
            "rank_org": properties.get("rank_org", ""),
            "num_employees_enum": properties.get("num_employees_enum", ""),
            "num_contacts": properties.get("num_contacts", ""),
            "job_posting_link_source": properties.get("job_posting_link_source", ""),
            "num_funding_rounds": properties.get("num_funding_rounds", ""),
            "categories": ", ".join([category.get("value", "") for category in properties.get("categories", [])]),
            "location_identifiers": ", ".join([location.get("value", "") for location in properties.get("location_identifiers", [])]),
            "num_event_appearances": properties.get("num_event_appearances", ""),
            "twitter": properties.get("twitter", {}).get("value", ""),
            "acquisition_announced_on": properties.get("acquisition_announced_on", {}).get("value", ""),
            "num_exits": properties.get("num_exits", ""),
            "rank_org_company": properties.get("rank_org_company", ""),
            "funding_stage": properties.get("funding_stage", "")
        }
        
        # Write the row to the CSV file
        writer.writerow(row)

print(f"CSV file '{csv_file}' has been created successfully.")
