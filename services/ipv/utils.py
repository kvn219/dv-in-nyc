# utils.py
from num2words import num2words


def filter_digits(func):
    def wrapper(filename):
        filename_digits = [char for char in filename if char.isdigit()]
        return func(filename_digits)
    return wrapper


@filter_digits
def check_monthly_radio_runs(filename_digits):
    return len(filename_digits) == 6


@filter_digits
def check_nycha_precinct(filename_digits):
    return len(filename_digits) == 5


@filter_digits
def check_nycha_psa(filename_digits):
    return len(filename_digits) == 4


def street_to_url(num):
    precincts_translation = {
        '22nd': 'central-park',
        '18th': 'midtown-north',
        '14th': 'midtown-south',
    }
    street = num2words(num, to='ordinal_num')
    lookups = precincts_translation.keys()
    if street in lookups:
        street = precincts_translation[street]
    url = f"http://www1.nyc.gov/site/nypd/bureaus/patrol/precincts/{street}-precinct.page"
    return url


def infer_borough(precinct):
    precinct = int(precinct)
    if 1 <= precinct <= 34:
        return 'manhattan'
    elif 35 <= precinct <= 52:
        return 'bronx'
    elif 40 <= precinct <= 94:
        return 'brooklyn'
    elif 100 <= precinct <= 115:
        return 'queens'
    elif 120 <= precinct <= 123:
        return 'staten island'
    else:
        raise Exception('Borough not found')
