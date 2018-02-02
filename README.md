# The data behind intimate partner violence in NYC

<p align="center">
  <br>
  <img src="map.gif">
  <br>
  View it <a href="https://kvn219.github.io/sdgs/">here.</a>
</p>


## Map
http://bit.ly/2EnznPe

## Question
What do reported incidents of intimate partner violence convey about geographic inequalities in NYC?

## About
While violent crimes in New York City has dropped precipitously since the early 1990s, domestic violence remains an ongoing and underreported problem, most commonly found in the form of Intimate Partner Violence (IPV). [According to the CDC](https://www.cdc.gov/violenceprevention/index.html), one out of four women in the U.S. has experienced an incident of domestic violence by an intimate partner. In NYC, it’s estimated that nearly [352,000](https://www1.nyc.gov/assets/criminaljustice/downloads/pdfs/domestic-violence-task-force-2017-recommendations.pdf) residents are victimized by an intimate partner each year.

Incidents of domestic violence or intimate partner violence affect every neighborhood in the city, with varying degree of incidents reported at the local level, as filed under official precinct data.

This project aggregates and visualizes data on domestic violence incidents collected by the NYPD from January through September 2017––we’ll update the map to correspond with incoming data. 


## Sources
[NYPD Domestic Violence Reports](https://www1.nyc.gov/site/nypd/stats/reports-analysis/domestic-violence.page)

[NYPD Precinct Map](https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts/1st-precinct.page)

[Map of NYCHA Developments](https://data.cityofnewyork.us/Housing-Development/Map-of-NYCHA-Developments/i9rv-hdr5)

# Running the project

## Requirements

- python 3

If you havent, you'll need to set up [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

### Clone the repo and setup the environment
```bash
git clone https://github.com/kvn219/ipv.git
```

### Go into the directory we just downloaded
```bash
cd ipv
```

### Create a virtual environment
```bash
virtualenv -p python3 venv
```

### Activate the virtual environment
```bash
source venv/bin/activate
```

### Install the required packages
```bash
pip install requirements.txt
```


### Run the program!
```bash
make run
```
