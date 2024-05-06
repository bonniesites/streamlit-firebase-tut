import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from pprint import pprint
import pandas as pd
import schedule
import time

from mods.header import * 
from mods.models import *
from mods.data_processing import *
from mods.utils import *

if not 'track_category' in st.session_state:
    st.session_state.track_category = ''

if not 'track_timer_running' in st.session_state:
    st.session_state.track_timer_running = False

if not 'time_started' in st.session_state:
    st.session_state.time_started = ''

# MongoDB setup
DB = CLIENT.time_tracker
TIMESTAMP_RECORDS = DB.records
DATA = list(TIMESTAMP_RECORDS.find())

st.write('TODO: EDIT SCREEN FOR TIMER RECORDS')

test_docs = list(TIMESTAMP_RECORDS.find().limit(5))
#print("\n\n Sample Documents:\n\n")
for doc in test_docs:
    pass
    #pprint(doc)
print('\n\n')

count_documents_with_start = TIMESTAMP_RECORDS.count_documents({'start': {'$exists': True}})
#st.write(f"Documents with 'start' field: {count_documents_with_start}")

# Test Pipeline
test_pipeline = [
    {
        '$match': {
            'start': {'$exists': True}
        }
    },
    {
        '$project': {
            'formattedDate': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$start"}},
            'weekNumber': {'$isoWeek': "$start"},
            'yearNumber': {'$isoWeekYear': "$start"},
            'originalStart': '$start'  # Include the original date for comparison
        }
    },
    {
        '$limit': 10  # Limit the documents for testing purposes
    }
]

results = TIMESTAMP_RECORDS.aggregate(test_pipeline)
for result in list(results):
    pass
    #st.write(result)
    #pprint(result)

def save_time(category, action):
    if action == 'start':
        # Stop any currently running timers
        current_record = TIMESTAMP_RECORDS.find_one({'end': None})
        if current_record:
            TIMESTAMP_RECORDS.update_one({'_id': current_record['_id']}, {'$set': {'end': datetime.now()}})
        # Start a new timer
        record = { 'start': datetime.now(), 'end': None, 'category': category }
        TIMESTAMP_RECORDS.insert_one(record)
        st.session_state.time_started = record['start']
        st.session_state.track_category = record['category']
        return record['_id'], record['start']
    elif action == 'stop':
        last_record = TIMESTAMP_RECORDS.find_one({'end': None, 'category': category})
        if last_record:
            TIMESTAMP_RECORDS.update_one({'_id': last_record['_id']}, {'$set': {'end': datetime.now()}})

def view_times():
    return list(TIMESTAMP_RECORDS.find({}).sort('start', -1))

def convert_to_seconds(date_str):
    if date_str is None:
        return None
    # Correct format string to include hours, minutes, seconds, and microseconds
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    try:
        # Parse the string into a datetime object
        date_obj = datetime.strptime(str(date_str), date_format)
        # Convert datetime to seconds since Unix epoch (January 1, 1970)
        seconds_since_epoch = date_obj.timestamp()
        return seconds_since_epoch
    except ValueError as e:
        # Print the error if any
        print(f"Error parsing date: {e}")
        return None

def convert_seconds_to_time(seconds):
    # Calculate hours by integer division
    hours = seconds // 3600
    # Calculate remaining seconds after extracting hours
    seconds_remaining = seconds % 3600    
    # Calculate minutes from the remaining seconds
    minutes = seconds_remaining // 60
    return hours, minutes

def format_datetime(dt):
    if dt is None:
        return 'N/A'
    return dt.strftime("%Y-%m-%d %H:%M")

def get_daily_totals():
    TIMESTAMP_RECORDS = list(view_times())
    date_totals = {}
    for record in TIMESTAMP_RECORDS:
        if record['end'] and record['start']:
            date = record['start'].strftime('%Y-%m-%d')
            elapsed_time = record['end'] - record['start']
            if date not in date_totals:
                date_totals[date] = timedelta(0)
            date_totals[date] += elapsed_time
    for date, total in date_totals.items():
        hours, minutes = convert_seconds_to_time(total.seconds)
        st.write(f"{date}: {hours * 60 + minutes} min, ({round(hours, 0)} hrs {round(minutes, 0)} min)")

def get_weekly_totals():
    # MongoDB Aggregation Pipeline
    pipeline = [
        {
            '$match': {
                'start': {'$exists': True, '$ne': None},
                'end': {'$exists': True, '$ne': None},
                'category': {'$exists': True, '$ne': None}
            }
        },
        {
            '$addFields': {
                'duration': {
                    '$divide': [{'$subtract': ['$end', '$start']}, 1000 * 60 * 60]  # duration in hours
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'date': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$start"}},
                    'category': '$category'
                },
                'dailyCategoryDuration': {'$sum': '$duration'}
            }
        },
        {
            '$sort': {'categories.category': 1}  # Sort categories alphabetically
        },
        {
            '$group': {
                '_id': {
                    'date': '$_id.date'
                },
                'categories': {
                    '$push': {
                        'category': '$_id.category',
                        'duration': '$dailyCategoryDuration'
                    }
                },
                'dailyTotalDuration': {'$sum': '$dailyCategoryDuration'}
            }
        },
        {
            '$group': {
                '_id': {
                    'week': {'$isoWeek': {'$toDate': "$_id.date"}},
                    'year': {'$isoWeekYear': {'$toDate': "$_id.date"}}
                },
                'days': {
                    '$push': {
                        'date': '$_id.date',
                        'dailyTotal': '$dailyTotalDuration',
                        'categories': '$categories'
                    }
                },
                'weeklyTotalDuration': {'$sum': '$dailyTotalDuration'}
            }
            
        },
            
        {'$sort': {
            '_id.year': 1,
            'weeks.week': 1,
            'days.date': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'year': '$_id.year'
                },
                'weeks': {
                    '$push': {
                        'week': '$_id.week',
                        'days': '$days',
                        'weeklyTotal': '$weeklyTotalDuration'
                    }
                },
                'yearlyTotalDuration': {'$sum': '$weeklyTotalDuration'}
            }
        },
        {
            '$group': {
                '_id': None,
                'years': {
                    '$push': {
                        'year': '$_id.year',
                        'weeks': '$weeks',
                        'yearlyTotal': '$yearlyTotalDuration'
                    }
                },
                'totalDuration': {'$sum': '$yearlyTotalDuration'}
            }
        }
    ]
    # Execute the aggregation pipeline
    results = TIMESTAMP_RECORDS.aggregate(pipeline)
    # Convert CommandCursor data to a dictionary
    data = list(results)
    return data

def calc_totals(data):
    # Sort data by date, category
    for row in data:
        seconds = (end - start)
        st.write(f'seconds: {seconds} ')
        hours, minutes = convert_seconds_to_time(seconds)


# year1, week1, day1, cat1, cat_total, date_total, week_total, year_total, grand_total
def display_header():
    with week1:
        st.write('Wk#')
    with day1:
        st.write('Date')
    with cat1:
        st.write('Cat')
    with cat_total: 
        st.write('Cat Total')
    with date_total: 
        st.write('Day Total')
    with week_total:  
        st.write('Wk Total') 
    with year_total:
        st.write('Yr Total')           
    with grand_total:
        st.write('All Time')

group_bys = ['day_cat', 'daysub', 'weekcat', 'weeksub', 'yearcat', 'yearsub', 'grand']

def print_totals(data):
    # Check if data is available
    if data:
        st.write(data)
        # Define column headers
        headers = ['year', 'week', 'date', 'category', 'duration', 'dailyTotal', 'weeklyTotal', 'yearlyTotal', 'totalDuration']
        
        # Create columns to display the data
        cols = st.columns(len(headers))
        
        # Set headers for each column
        for i, header in enumerate(headers):
            cols[i].write(header)
        
        # Iterate over each row of data and display it in columns
        for row in data:
            for i, header in enumerate(headers):
                # st.write(f'header: {header}: {row[header]}')
                # Check if the header exists in the row data
                if header in row:
                    if row[header] > 0:
                        hours, minutes = convert_seconds_to_time(row[header] * 3600) 
                        # Write the corresponding data to the column
                        cols[i].write(f" {hours} hr {minutes} min")
                    else:
                        cols[i].write(row[header])
                else:
                    # If the header doesn't exist in the row, write an empty cell
                    cols[i].write('')
    else:
        st.write("No data available.")


 
def display_time_row(line):
    st.write(f'line: {line}')
    for idx, row in line.iterrows():
        hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
        with week1:
            if "Week Number" in row:
                st.write(str(row['Week Number']))
        with day1:
            if "Date" in row:
                st.write(row['Date'])
        with cat1:
            if "Category" in row:
                st.write(row['Category'])
        with cat_total:            
            st.write(f" {hours} hr {minutes} min")
        with date_total:
            st.write(f" {hours} hr {minutes} min")
        with week_total: 
            st.write(f" {hours} hr {minutes} min")  
        with year_total:
            st.write(f" {hours} hr {minutes} min")      
        with grand_total: 
            st.write(f" {hours} hr {minutes} min")
    # st.dataframe(category_subtotal_per_day)

def display_aggregate_data(results):
    # Define lists to store the data 
    date_list = []
    category_list = []
    week_number_list = []
    subtotal_list = []

    # Iterate over the results to extract the data
    for year_data in results[0]['years']:
        for week_data in year_data['weeks']:
            for day_data in week_data['days']:
                date = day_data['date']
                week_number = week_data['week']
                daily_subtotal = day_data['dailyTotal']
                # Append data for category subtotal per day
                for category_data in day_data['categories']:
                    category = category_data['category']
                    subtotal = category_data['duration']
                    date_list.append(date)
                    category_list.append(category)
                    week_number_list.append(week_number)
                    subtotal_list.append(subtotal)


    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Date': date_list,
        'Category': category_list,
        'Week Number': week_number_list,
        'Subtotal': subtotal_list
    })

    # Calculate subtotal per category per day
    category_subtotal_per_day = df.groupby(['Date', 'Category']).sum().reset_index()

    # Calculate subtotal per day
    subtotal_per_day = df.groupby('Date')['Subtotal'].sum().reset_index()

    # Calculate subtotal per category per week
    category_subtotal_per_week = df.groupby(['Week Number', 'Category']).sum().reset_index()
    st.write(f'category_subtotal_per_week: {category_subtotal_per_week}')

    # Calculate subtotal per week
    subtotal_per_week = df.groupby('Week Number')['Subtotal'].sum().reset_index()

    # Calculate subtotal per category per year
    category_subtotal_per_year = df.groupby(['Date', 'Category']).sum().reset_index()
    category_subtotal_per_year['Year'] = pd.to_datetime(category_subtotal_per_year['Date']).dt.year

    # Calculate subtotal per year
    subtotal_per_year = df.groupby('Date')['Subtotal'].sum().reset_index()
    subtotal_per_year['Year'] = pd.to_datetime(subtotal_per_year['Date']).dt.year
    print('')
    print('')
    print(f"subtotal_per_year['Year']: {subtotal_per_year['Year']}")
    print('')
    print('')
    print('')

    # Calculate subtotal for all time
    subtotal_all_time = df['Subtotal'].sum()

       # Display the results
    st.subheader("Category Subtotal per Day")
    display_header()
    display_time_row(category_subtotal_per_day)    

    st.subheader("Subtotal per Day")
    #for idx, row in subtotal_per_day.iterrows():    
    display_header()
    display_time_row(subtotal_per_day) 
    #hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
    #with date_total:
    #        f"{row['Date']}: {hours} hr {minutes} min"

    # st.dataframe(subtotal_per_day)
    #for idx, row in category_subtotal_per_week.iterrows():    
    display_header()
    display_time_row(category_subtotal_per_week) 
        ##hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
        #st.write(f"{row['Week Number']-16}, {row['Category']},  {hours} hr {minutes} min")

    st.subheader("Subtotal per Week")   
    display_header()
    display_time_row(subtotal_per_week) 
    #for idx, row in subtotal_per_week.iterrows():
     #   hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
      #  st.write(f"{row['Week Number']-16} {hours} hr {minutes} min")

    st.subheader("Category Subtotal per Year")   
    display_header()
    display_time_row(category_subtotal_per_year) 
    #for idx, row in category_subtotal_per_year.iterrows():
     #   hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
      #  st.write(f"{row['Year']}  {row['Category']} {hours} hr {minutes} min")

    st.subheader("Subtotal per Year")   
    display_header()
    display_time_row(category_subtotal_per_year) 
    #for idx, row in subtotal_per_year.iterrows():
     #   hours, minutes = convert_seconds_to_time(row['Subtotal'] * 3600)
      #  st.write(f"{row['Year']}, {hours} hr {minutes} min")

    
    st.subheader("Grand Total")     
    display_header()
    hours, minutes = convert_seconds_to_time(subtotal_all_time * 3600)    
    st.write(f" {hours} hr {minutes} min")
    #hours, minutes = convert_seconds_to_time(subtotal_all_time * 3600)
    #st.subheader(f"Subtotal for All Time: {hours} hr {minutes} min")

def send_notification():
    # Code to send notification using a chosen service
    st.write("Notification sent!")

# Schedule notification every 15 minutes
schedule.every(15).minutes.do(send_notification)


def my_attempt_fix_display(data):
    # Print the data
    print("\n\nAggregated Time Tracking Data:\n\n")
    pprint(data)
    for result in list(data):        
        pprint(result)
    print('\n\n')
    st.subheader("Aggregated Time Tracking Data:")
    # Display total duration
    #st.write(f"Total Hours: {round(data[0]['totalDuration'], 0)}")
    col1, col2, col3, col4, col5 = st.columns(5)
    # Loop through years
    for year_data in data[0]['years']:
        # Loop through weeks
        for week_data in year_data['weeks']:
            # Loop through days
            for day_data in week_data['days']:
                with col1:
                    st.write(day_data['date'])
                # Loop through categories
                for category_data in day_data['categories']:
                    with col2:
                        st.write(f"{category_data['category']}: {round(category_data['duration'], 0)}")
            with col3:
                st.write(f"Total: {round(day_data['dailyTotal'], 0)}")
            #st.write(f"Week: {week_data['week']}")
            st.write(f"WK {week_data['week']} Hours: {round(week_data['weeklyTotal'], 0)}")
        #st.write(f"Year: {year_data['year']}")
        st.write(f"{year_data['year']} Hours: {round(year_data['yearlyTotal'], 0)}")

def list_times():
    st.subheader("Logged Times:")
    start_col, stop_col, cat, time = st.columns(4)
    with start_col:
        'Start Time'
    with stop_col:
        'Stop Time'
    with cat: 
        'Category'
    with time:
        'Time'
    total = 0
    week_total = 0
    day_total = 0
    for record in view_times():
        #for year in record['end']:
        if not record.get('end') == None:
            start = format_datetime(record.get('start'))
            stop = format_datetime(record.get('end'))
            start_seconds = convert_to_seconds(record.get('start'))
            stop_seconds = convert_to_seconds(record.get('end'))
            elapsed_seconds = stop_seconds - start_seconds
            hours, minutes = convert_seconds_to_time(elapsed_seconds)
            #print(f"Time elapsed = {hours}:{minutes}.")
            with start_col:
                start
            with stop_col:
                stop
            with cat:
                if record['category']:
                    record['category']
                else:
                    ''
            with time:
                f"{hours * 60 + minutes} min, ({round(hours, 0)} hrs {round(minutes, 0)} min)"
        #st.write(f"Start: {start} - End: {stop} | TIME ELAPSED: {int(hours)}:{int(minutes)}")

def display_times():
    TIMESTAMP_RECORDS = list(view_times())
    totals = {cat: timedelta(0) for cat in categories}
    for record in TIMESTAMP_RECORDS:
        if record['end'] and record['start']:
            elapsed_time = record['end'] - record['start']
            totals[record['category']] += elapsed_time

    for category, total in totals.items():
        hours, remainder = divmod(total.seconds, 3600)
        minutes = remainder // 60
        st.write(f"{category}: {int(hours)} hours and {int(minutes)} minutes total")

categories = ['Coding', 'Consulting', 'Learning', 'Reporting']
end_dates = ['2024-04-27', '2024-05-04', '2024-05-11', '2024-05-18',
 '2024-05-25', '2024-06-01', '2024-06-08', '2024-06-15', '2024-06-22', 
 '2024-06-29', '2024-07-06', '2024-07-13', '2024-07-20']

st.title('VS Code Time Tracker')

if st.session_state.track_timer_running == True:
    seconds_elapsed = datetime.now() - st.session_state.time_started
    current_timer_minutes = seconds_elapsed.total_seconds() // 60
    print('current_timer_minutes', current_timer_minutes)
    print('st.session_state.track_timer_running', st.session_state.track_timer_running)
    #formatted_timer_total = round(current_timer_minutes, 0)
    st.warning(f"Timer running for {st.session_state.track_category} has {current_timer_minutes} minutes now!")

for category in categories:
    with st.container():
        timer_placeholder = st.empty()
        start_button, stop_button = st.columns(2)            
        with start_button:
            if st.button(f'Start {category}', key=f'start_{category}'):
                record_id = save_time(category, 'start')
                st.session_state.track_category = category
                st.session_state.track_timer_running = True
                st.success(f"Timer started for {st.session_state.track_category} with record ID: {record_id}")
        with stop_button:
            if st.button(f'Stop {category}', key=f'stop_{category}'):
                if st.session_state.get('track_timer_running', False) and st.session_state.get('track_category', '') == category:
                    save_time('st.session_state.track_category', 'stop')
                    st.session_state.track_timer_running = False
                    st.error(f"Timer stopped for {st.session_state.track_category}.")

def print_totals2(data):
    # Convert data to DataFrame
    df = pd.DataFrame.from_records(data)
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])

    # Calculate duration
    df['duration'] = df['end'] - df['start']

    # Group by category, day, and week
    df['day'] = df['start'].dt.date
    df['week'] = df['start'].dt.strftime('%Y-%W')
    
    grouped = df.groupby(['day', 'category']).agg({'duration': 'sum'}).reset_index()

    # Calculate subtotals
    subtotals_per_category_per_day = grouped.pivot(index='day', columns='category', values='duration')
    subtotal_per_day = grouped.groupby('day')['duration'].sum()
    subtotals_per_category_per_week = df.groupby(['week', 'category'])['duration'].sum().reset_index().pivot(index='week', columns='category', values='duration')
    subtotal_per_week = df.groupby('week')['duration'].sum().apply(convert_seconds_to_time)
    grand_total = df['duration'].sum()

    # Display in Streamlit columns
    st.write("Subtotals each category per day:")
    st.write(subtotals_per_category_per_day)
    # cat_day_hours, cat_day_minutes = convert_seconds_to_time(subtotals_per_category_per_day)
    # st.write(f'{cat_day_hours} hrs, {cat_day_minutes} min')

    st.write("Subtotal per day:")
    st.write(subtotal_per_day)

    st.write("Subtotals each category per week:")
    st.write(subtotals_per_category_per_week)

    st.write("Subtotal per week:")
    st.write(subtotal_per_week)

    st.write("Grand Total:")
    st.write(grand_total)

printtotal, daily, weekly, listtimes = st.columns(4)
with printtotal:
    printbtn = st.button('Print Totals', type='primary')
with daily:
    dailybtn = st.button('Daily Totals', type='primary')
with weekly:
    get_totals = st.button('Weekly Totals', type='primary')
with listtimes:
    listbtn = st.button('List daily time records', type='primary')

if printbtn:
    print_totals2(DATA)
if daily:
    get_daily_totals()

if get_totals:
    total_box = st.empty()
    week1, day1, cat1, cat_total, date_total, week_total, year_total, grand_total = st.columns([2,4,4,4, 4,4,4,4])        
    display_aggregate_data(get_weekly_totals())
if listbtn:
    list_times()

if st.session_state.track_timer_running == True:
    st.warning(f"Timer running for {st.session_state.track_category}!")





'TODO: SET NOTIFICATIONS/REMINDERS FOR OVER 1 HOUR'
'TODO: get subtotals per category, totals per day'
'TODO: get subtotals per category, totals per week, using week ending date list'
    

if st.session_state.track_timer_running == True:
    st.warning(f"Timer running for {st.session_state.track_category}!")






# # Placeholders for the timer and buttons
# timer_placeholder = st.empty()
# start_button, stop_button = st.columns(2)
    
# with start_button:
#     if st.button('Start Coding'):
#         record_id = save_time('start')
#         # Store the start time in the session state
#         st.session_state.start_time = datetime.now()
#         st.session_state.track_timer_running = True
#         st.write(f"Timer started for record ID: {record_id}")
#         # elapsed = convert_to_seconds() - convert_to_seconds()
#         # st.write(f'Time elapsed: {}')
# with stop_button:
#     if st.button('Stop Coding'):
#         st.session_state.track_timer_running = False
#         save_time('stop')
#         st.write("Timer stopped.")
#         # Check if the timer is running
#         if st.session_state.get('track_timer_running', False):
#             # While the timer is running, update the elapsed time
#             while st.session_state.get('track_timer_running', False):
#                 elapsed = datetime.now() - st.session_state.start_time
#                 timer_placeholder.markdown(f'**Elapsed Time:** {str(elapsed).split(".")[0]}')
#                 time.sleep(1)  # Refresh every second



