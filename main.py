from py.constants import *
from py.classes import *
from py.credentials import *
import csv, json

with open('dataset/Stogsstationer.csv', newline='', encoding = 'utf-8') as csvfile:
    data = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    current_time, current_date, train_arriving = Time.converter() # Define current time, date and arrival

    global all_departures
    all_departures = []
    
    for station in data:
        stop_id = station['stop_id'] # Get station id from csv
        APICall.get_station(stop_id, current_time, current_date, USERNAME, PASSWORD) # Parse stop to xml
        timetable = Station.parse_xml_to_dict(stop_id, train_arriving) # Parse xml to dict
        all_departures.extend(timetable) # Parse data to local dict

with open('dataset/train_lines.json') as train_lines:
    lines_data = json.load(train_lines)
    stopped_trains = Station.get_stopped_trains(all_departures, current_time)
    arriving_trains = Station.get_arriving_trains(all_departures, train_arriving)

    stops_index, arrivals_index = LEDStrip.id_to_index(lines_data, stopped_trains, arriving_trains)

"""
Current output example:
stops_index = {'a_line': [0, 32, 14, 24],
 'b_line': [10, 23, 17, 25, 16, 1],
 'bx_line': [7, 26, 14, 13, 1], 
 'c_line': [21, 14, 27, 15],
 'e_line': [11, 26, 8, 18],
 'f_line': [7, 11, 1],
 'h_line': [13, 6, 7]}
"""