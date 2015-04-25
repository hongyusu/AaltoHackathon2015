

**Get general track information**
==
  track_basic_information_extraction.py		parse track information, extract track global information about tracks


**Basic track information**
==
  file: file_first_gps.txt

  select all tracks with lng/lat information

  format: trackname lng lat sportname username distance


**select tracks based on city**
==
  file: track_selection.py


**generate KML file for tracks of a city**
==
  file: compute_kml_from_track_basic_information.py


**Coordinate system format**
==
  raw data 			(x,y) 		(lng,lat)

  city data 		(y,x) 		(lat,lng)

  KML				(x,y) 		(lng,lat)