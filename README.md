# Getting data behind intimate partner violence in NYC

[![Build Status](https://travis-ci.org/kvn219/ipv.svg?branch=master)](https://travis-ci.org/kvn219/ipv)

View map [here](http://bit.ly/2EnznPe)

## About

While violent crimes in New York City has dropped precipitously since the early 1990s, domestic violence remains an ongoing and underreported problem, most commonly found in the form of Intimate Partner Violence (IPV). [According to the CDC](https://www.cdc.gov/violenceprevention/index.html), one out of four women in the U.S. has experienced an incident of domestic violence by an intimate partner. In NYC, it’s estimated that nearly [352,000](https://www1.nyc.gov/assets/criminaljustice/downloads/pdfs/domestic-violence-task-force-2017-recommendations.pdf) residents are victimized by an intimate partner each year.

Incidents of domestic violence or intimate partner violence affect every neighborhood in the city, with varying degree of incidents reported at the local level, as filed under official precinct data.

This project aggregates and visualizes data on domestic violence incidents collected by the NYPD from January through September 2017––we’ll update the map to correspond with incoming data.

## Problem

Data for reported rates of domestic violence in NYC are available on the NYPD's website. Unfortunately, its in a format not useful for programmatic analysis and mapping (Monthly reports are in individual csv files). If we wanted to summarize statistics for the year, we would have to manually download all the files. And merge them ourselves.

Another problem with the data is the precinct information. We are only given a number between 1 and 123 to identify the precinct. Unless we're deeply invested in the NYPD, its very hard to contextualize where each precinct is in NYC.

## Project

This project shows how I've programmatically solve these problems. I started by downloading and merging monthly reports from the [NYPD Domestic Violence reports webpage](https://www1.nyc.gov/site/nypd/stats/reports-analysis/domestic-violence.page). Next, I enriched precinct information by scraping details from [public precinct websites](https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts/1st-precinct.page). To prepare mapping data, I merged the aggregated data to the [boundaries of NYC's police precincts](https://data.cityofnewyork.us/api/geospatial/78dh-3ptz?method=export&format=GeoJSON). And finally I used [Carto](http://bit.ly/2EnznPe) to create a nice interactive map.

## Data Sources

* [NYPD Domestic Violence Reports](https://www1.nyc.gov/site/nypd/stats/reports-analysis/domestic-violence.page)

* [NYPD Precinct Map](https://data.cityofnewyork.us/api/geospatial/78dh-3ptz?method=export&format=GeoJSON)

* [NYPD Precincts](https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts-landing.page)

* [Example of NYPD Precinct Information](https://www1.nyc.gov/site/nypd/bureaus/patrol/precincts/1st-precinct.page)

* [Map of NYCHA Developments](https://data.cityofnewyork.us/Housing-Development/Map-of-NYCHA-Developments/i9rv-hdr5)

## Getting started

To get started with the project, you need to have [Python 3](https://www.python.org/downloads/source/) and [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) set up on your local machine.

**Clone the repo and setup the environment**

```bash
git clone https://github.com/kvn219/ipv.git
```

**Move into the ipv directory**

```bash
cd ipv
```

**Create a virtual environment**

```bash
virtualenv -p python3 venv
```

**Activate the virtual environment**

```bash
source venv/bin/activate
```

**Install the required packages**

```bash
pip install requirements.txt
```

**Run the program!**

```bash
make run
```

## Docker

If you're comfortable with docker and make, you can run the following commands:

```bash
make docker_build
make docker_run
```

## Example use case

[Create a choropleth Bokeh!](http://nbviewer.jupyter.org/github/kvn219/ipv/blob/master/notebooks/UseCases.ipynb)
