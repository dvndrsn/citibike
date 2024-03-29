# Citi Bike Trip History

A simple project to work with Citi Bike data showing every trip bike #77139 took in August 2015 in NYC.

<img width="860" alt="citibike" src="https://github.com/dvndrsn/citibike/assets/4897035/f453fb72-a54a-496f-a200-ff5a0c19374f">

Citibike system data is available for download [here][citibike-system-data].

[citibike-system-data]: https://citibikenyc.com/system-data

We started with one month's system data. The data was then processed and filtered using iPython notebooks, pandas and numpy to extract stations locations and bike trips.

TOPOjson is leveraged to draw features of the NYC region and mark the location of the [Recurse Center][rc], where Dave Anderson and Aliza Aufrichtig created this visualization in Winter 2015/2016.

[rc]: https://recurse.com

# References

This project uses:
- https://commons.wikimedia.org/wiki/File:Upright_urban_bicyclist.svg
- https://s3.amazonaws.com/tripdata/201508-citibike-tripdata.zip
