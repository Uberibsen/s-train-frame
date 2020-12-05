from py.constants import *
import datetime
import requests
import xmltodict
import xml
import json

class Time:
    def converter():
        """Converts current time and date to specified format"""
        current_time = datetime.datetime.now() # Fetch time
        time_formatted = current_time.strftime(TIME_FORMAT) # Format to string in HH:MM format
        current_date = datetime.date.today() # Fetch date
        date_formatted = current_date.strftime(DATE_FORMAT) # Format to string in DD:MM:YY format 
        nextstop = current_time + datetime.timedelta(minutes = 1) # Define variable with one minute added before train arriving
        train_arriving = nextstop.strftime(TIME_FORMAT) # Format to string in HH:MM format

        return time_formatted, date_formatted, train_arriving

class APICall:
    def __init__(self, stop_id, current_time, current_date, USERNAME, PASSWORD):
        """Initialize the data object."""
        self.stop_id = stop_id
        self.current_time = current_time
        self.current_date = current_date
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD

    def get_station(stop_id, current_time, current_date, USERNAME, PASSWORD):
        """Imports one stop based on id, date and time"""
        response = requests.get(BASE_URL +
                '/departureBoard?id=' + str(stop_id) + # Station ID
                '&date=' + str(current_date) + # Departure date
                '&time=' + str(current_time) + # Departure time
                '&useBus=0', # Additional arguments (Don't import busses, only trains)
                auth = (USERNAME, PASSWORD)) # Credentials
        if response.status_code == 200:
            with open('xml/data.xml', 'w', encoding = "utf-8") as f:
                f.write(response.text)
        else:
            raise ConnectionError

class Station:
    def __init__(self, stop_id, departures, arriving_status, time):
        """Initialize the data object."""
        self.stop_id = stop_id
        self.departures = departures
        self.arriving_status = arriving_status
        self.time = time

    def parse_xml_to_dict(stop_id, train_arriving):
        """Parses xml data from the departures to a list for further use"""
        with open('xml/data.xml', encoding = "utf-8") as fd:
            station_info = xmltodict.parse(fd.read())

            timetable = []
            try:
                for departure in station_info['DepartureBoard']['Departure']:
                    if "S" in departure['@type']:
                        train = {'line': departure['@line'],
                            'station': departure['@id'],
                            'departure': departure['@time'],
                            'finalStop': departure['@finalStop']}
                        if train_arriving in departure['@time']:
                            train['train_arriving'] = True
                        else:
                            train['train_arriving'] = False
                        timetable.append(train)
            except KeyError:
                train = {'station': stop_id,
                    'error': station_info['DepartureBoard']['@error']}
                timetable.append(train)
            return timetable
    
    def get_stopped_trains(departures, current_time):
        """Takes all departures and extracts the stops with trains present"""
        stops_with_trains = []
        for stop in departures:
            if current_time in stop['departure']:
                station_with_stop = stop['station']
                stops_with_trains.append(station_with_stop)
        return stops_with_trains

    def get_arriving_trains(departures, arriving_status):
        """Checks if a train is arriving at a station"""
        trains_arriving = []
        for stop in departures:
            if stop['train_arriving'] == True:
                has_train_arriving = stop['station']
                trains_arriving.append(has_train_arriving)
        return trains_arriving

class LEDStrip:
    def __init__(self, data, stopped_trains, arriving_trains):
        self.data = data
        self.stopped_trains = stopped_trains
        self.arriving_trains = arriving_trains

    def id_to_index(data, stopped_trains, arriving_trains):
        """Takes all stopped and arriving trains id's and takes their position on the respective route"""
        stops_index = {}
        arrivals_index = {}
        for l in (data['lines']): # Create (or empty) lists of all lines within a dictionary
            stops_index[str(l)] = []
            arrivals_index[str(l)] = []

        for line in stops_index.keys(): # For each line...
            current_line = data['lines'][line]
            for station_id in stopped_trains: # ...of stopped trains...
                if int(station_id) in current_line: # ...check if the station appear on that line...
                    station_index = current_line.index(int(station_id)) # ...and take the index of that station...
                    stops_index[line].append(station_index) # ...and append it to the respective line

        for line in arrivals_index.keys(): # Same functionality of previous loop but with arriving trains
            current_line = data['lines'][line]
            for station_id in arriving_trains:
                if int(station_id) in current_line:
                    station_index = current_line.index(int(station_id))
                    arrivals_index[line].append(station_index)      
        return stops_index, arrivals_index

    def display_stopped_trains(self, stops_index):
        """
        Makes the individual lights of the LED strip glow steady for each
        train stopped
        """
        raise NotImplementedError

    def display_arriving_trains(self, arrivals_index):
        """
        Makes the individual lights of the LED strip pulse for each
        train arriving
        """
        raise NotImplementedError

# TODO
# Optimize xml_to_dict_parse only to loop a certain amount of times (5-10 departures)