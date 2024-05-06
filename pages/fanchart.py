import streamlit as st
import pandas as pd
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from io import BytesIO
import tempfile
import os
import matplotlib.pyplot as plt
from pymongo import MongoClient


# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the GEDCOM file
GEDCOM_FILE_PATH = os.path.join(current_dir, "gedfiles", "lincoln.ged")
    
# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
# Setup MongoDB client
DB = client['lfha']
# Get all documents in goals collection
PEOPLE = DB['people']

def get_individuals(file_path):
    # Initialize the parser
    gedcom_parser = Parser()
    # Parse your file (False denotes turning strict parsing off)
    gedcom_parser.parse_file(GEDCOM_FILE_PATH, False) 
    root_child_elements = gedcom_parser.get_root_child_elements()
    return root_child_elements

def list_names(name_list):
    # Extract individuals from the parsed GEDCOM data
    for individual in name_list:
        f'INDIVIDUAL: {individual}'
    
def save_to_mongodb(collection, data):
    collection.insert_many(data)



def main():
    # Parse the GEDCOM file
    parsed_gedcom = get_individuals(GEDCOM_FILE_PATH)
    individuals = list_names(parsed_gedcom)

    # Save parsed data to MongoDB
    save_to_mongodb(PEOPLE, individuals)
    
    
with st.sidebar:
    parsed_file = get_individuals(GEDCOM_FILE_PATH)
    people = list_names(parsed_file)
    # Iterate through all root child elements
    for element in parsed_file:
        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):
            # # Get all individuals whose surname matches search_term
            # if element.surname_match('l*'):
            #     # Unpack the name tuple
            #     (first, last) = element.get_name()
            #     birth = element.get_birth()
            #     # Print the first and last name of the found individual
            #     st.write(first + " " + last)
                       
            # Unpack the name tuple
            (first, last) = element.get_name()
            #birth = element.get_birth()
            # Print the first and last name of the found individual
            st.write(first + " " + last)
            st.write(element)

if __name__ == "__main__":
    main()



# # Function to parse GEDCOM file and extract data

# def parse_gedcom(file):
#     individuals = []
#     parser = Parser()

#     try:
#         # Save the content of the BytesIO object to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#             temp_file.write(file.getvalue())
#             temp_file_path = temp_file.name
        
#         # Parse the GEDCOM file
#         gedcom = parser.parse_file(temp_file_path)

#         # Check if parsing was successful
#         if gedcom is None:
#             raise ValueError("Failed to parse GEDCOM file")
        
#         # Process the parsed data
#         for i in gedcom.individuals:
#             # Check if birth date information is available
#             birth_date = i.birth_date if i.birth_date else None
            
#             individuals.append({
#                 "id": i.individual_id,
#                 "name": i.name,
#                 "birth_date": i.birth_date,
#                 "death_date": i.death_date,
#                 "parents": i.parents,
#                 "children": i.children
#             })
#         st.write(i.individual_id)
#         st.write(i.name)
#         st.write(i.birth_date)
#         st.write(i.death_date)
#         st.write(i.parents)
#         st.write(i.children)

#     except Exception as e:
#         # Handle parsing errors
#         print(f"Error parsing GEDCOM file: {e}")
#         individuals = None
    
#     finally:
#         # Remove the temporary file
#         os.unlink(temp_file_path)
    
#     return individuals


# # Function to create ancestry fan chart
# def create_fan_chart(individuals):
#     # Your code to create the fan chart goes here
#     # You can use plotting libraries like matplotlib or plotly to create the chart
    
#     if individuals is None:
#         print("Error: No individuals data to create the fan chart.")
#         return

#     # Example: Create a DataFrame with individual data
#     df = pd.DataFrame(individuals)
    
#     # Example: Plot the fan chart using matplotlib
#     # Replace this with your actual fan chart creation code
#     st.write(df)
    
#     # Create a fan chart using Matplotlib
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # Your code to create the fan chart goes here
#     # Example:
#     ax.plot(df['birth_date'], df['name'], marker='o', linestyle='-')
#     ax.set_xlabel('Birth Date')
#     ax.set_ylabel('Name')
#     ax.set_title('Ancestry Fan Chart')
#     ax.grid(True)
    
#     # Show the fan chart
#     st.pyplot(fig)

# # Main function
# def main():
#     st.title("Ancestry Fan Chart")
    
#     # Upload GEDCOM file
#     file = st.file_uploader("Upload GEDCOM file", type=["ged", "gedcom"])
    
#     if file is not None:
#         individuals = parse_gedcom(file)
#         st.write("Parsed individuals from GEDCOM file:")
#         st.write(individuals)
        
#         st.subheader("Ancestry Fan Chart")
#         create_fan_chart(individuals)

# if __name__ == "__main__":
#     main()


