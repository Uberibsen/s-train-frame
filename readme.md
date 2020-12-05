![GitHub last commit](https://img.shields.io/github/last-commit/uberibsen/s-train-frame)
![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen)

#  S-train live frame
This physical picture frame displays the current location of all S-trains in Denmark on their routes with the WS2812B LED strips. The idea is largely based on [DSB's](https://www.dsb.dk/) already excisting website [Byens Puls](https://www.rejseplanen.dk/bin/help.exe/mn?L=vs_livemap.vs_schematic&tpl=fullscreenmap&view=dsb&responsive=1&schematic=true). The program pulls data from [Rejseplanen](https://webapp.rejseplanen.dk/webapp/?language=en_EN) which is the official journey planner for public transport in Denmark. Their open [API](https://help.rejseplanen.dk/hc/da/articles/214174465-Rejseplanens-API) is used to request live traffic information from their database. 

## How the program works
Every minute, the program sends a request for all stations on the S-train network. Each station has a unique `id` and is referenced from an already excisting datasheet at `stations/Stogsstationer.csv`, fetched from the API documentation.

Each request can only bear the information from a single station. The request is then repeated for each station until all information from all stations are extracted. Every request in answered in the `xml` format and is locally saved in the `/xml` folder. From that saved file, `id`, `line`, `time` and `finalStop` is appended to the `timetable` dictionary and returned as a local variable.

### Example of request from API
```xml
<?xml version="1.0" encoding="UTF-8"?>
<DepartureBoard xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://webapp.rejseplanen.dk/xml/rest/hafasRestDepartureBoard.xsd">
<Departure name="B" type="S" stop="Albertslund St." time="22:01" date="01.12.20" id="8600621" line="B" messages="1" rtTrack="4" finalStop="Høje Taastrup St." direction="Høje Taastrup St.">
<JourneyDetailRef ref="http://webapp.rejseplanen.dk/bin//rest.exe/journeyDetail?ref=502704%2F192919%2F234768%2F50194%2F86%3Fdate%3D01.12.20" />
</Departure>
</DepartureBoard>
```

Once all departure information from all stations is locally saved in the `all_departures` dictionary, it is then checked whether or not the station in question has a train stopped at the platform, or if a train is arriving. The `all_departures` dictionary is looped through and checked if the current time - defined by the `current_time` variable - equals to the departure time. It is also checked if a train is arriving with the `train_arriving` varible, which is `current_time` subtracted one minute before departure. A list `stations_with_train` with all stations with arriving and departing trains.

From `stations_with_train`, all the id's are then mapped corresponding to the trainroutes from `stations/train_lines.json`. The final output is then a list for each of the lines with indexes as `stops_index`.
## Examples
### Final index output example
```python
stops_index = {'a_line': [1, 32, 14, 24],
 'b_line': [10, 23, 17, 25, 16, 1],
 'bx_line': [7, 26, 14, 13, 1], 
 'c_line': [21, 14, 27, 15],
 'e_line': [11, 26, 8, 18],
 'f_line': [7, 11, 1],
 'h_line': [13, 6, 7]}
```
*`stops_index` numbers cooresponds to the indexes below and each line have their own set in index numbers*
### Example of stops with cooresponding indexes
![](img\example.jpg "Line C, H, B and Bx on the S-train network")

## Physical construction
*The frame is currently under construction. More pictures and build files in a future release*