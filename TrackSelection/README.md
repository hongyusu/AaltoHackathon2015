

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


**location-specific sum of distance**
==
  file: loc2dist.py


**generate KML file for tracks of a city**
==
  file: compute_kml_from_track_basic_information.py


**Coordinate system format**
==
  raw data 			(x,y) 		(lng,lat)

  city data 		(y,x) 		(lat,lng)

  KML				(x,y) 		(lng,lat)

**Major cities and locations**
==
  file: 			city_gps.txt 			original data
  file: 			city_gps_refine.txt 	refined data
  format: 			cityname lat lng
  refine_city_gps.py 		refine original city data to refined data


**Add city information to track general information**
==
  file: 			assign_city_information.py 		assign city information
  file: 			file_first_gps_city.txt 		general track information with city information
  format: 			city___city___city
