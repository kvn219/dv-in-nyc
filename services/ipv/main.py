import time
import requests
import argparse
import numpy as np
import pandas as pd
import geopandas as gp
from datetime import datetime
from glob import glob
from pytz import timezone
from bs4 import BeautifulSoup
from num2words import num2words
from utils import (
    check_monthly_radio_runs,
    check_nycha_precinct,
    check_nycha_psa,
    street_to_url,
    infer_borough,
)


def get_user_args():
    # default url
    url = 'https://www1.nyc.gov/site/nypd/stats/reports-analysis/domestic-violence.page'
    parser = argparse.ArgumentParser(
        description="Downloads csv reports from OCDV's website"
    )
    parser.add_argument(
        '--url',
        default=url,
        help="URL to OCDV's website."
    )
    args, _ = parser.parse_known_args()
    return args


def grab_reports(args):
    page = fetch_page(args.url)
    html_items = parse(page)
    csv_urls = [url for url in grab_csv_urls(html_items)]
    radio_reports = filter(lambda url: check_monthly_radio_runs(url), csv_urls)
    precinct_reports = filter(lambda url: check_nycha_precinct(url), csv_urls)
    psa_reports = filter(lambda url: check_nycha_psa(url), csv_urls)
    return {
        'radio_reports': list(radio_reports),
        'precinct_reports': list(precinct_reports),
        'psa_reports': list(psa_reports),
    }


def fetch_page(url):
    request = requests.get(url).text
    page = BeautifulSoup(request,  'html.parser')
    return page


def parse(page):
    target = page.findAll("div", {"class": "about-description"})[0]
    html_items = target.find_all('li')
    return html_items


def grab_csv_urls(html_items):
    for item in html_items:
        a = item.find('a')
        yield a.attrs['href']


def fetch_report(link):
    URL = f"https://www1.nyc.gov{link}"
    expected_cols = [
        'Precinct',
        'Radio Runs',
        'Rape Complaints',
        'Felony Assault Complaints'
    ]
    # header starts five rows down.
    df = pd.read_excel(URL, header=5)
    df = df[expected_cols]
    return df.iloc[:-1, :]


def download(df, link):
    tz = timezone('US/Eastern')
    dt_fmt = '%Y-%m-%d %H:%M:%S %Z'
    filename = link.split('/')[-1]
    file_meta_data = filename.replace('.', '-').split('-')
    df['Month'] = file_meta_data[4]
    df['Year'] = file_meta_data[5]
    df['Source'] = f"https://www1.nyc.gov{link}"
    df['DateAccessed'] = datetime.now(tz=tz).strftime(dt_fmt)
    outfile = filename[:-5]
    outpath = f"./data/raw/{outfile}.csv"
    print(f"Downloading {outfile} to {outpath}")
    df.to_csv(outpath, index=False)


def merge():
    report_files = glob("./data/raw/*.csv")
    merged_df = pd.DataFrame()
    _frames = []
    for file in report_files:
        df = pd.read_csv(file, index_col=None, header=0)
        _frames.append(df)
    merged_df = pd.concat(_frames)
    n_precincts = 77
    n_months_in_2017 = len(report_files)
    n_rows, n_cols = merged_df.shape
    assert n_rows == n_precincts * n_months_in_2017
    assert n_cols == 8
    return merged_df


def extract_precinct_desc(street):
    time.sleep(.25)
    if street == 49:
        return (
            'The 49th Precinct serves a northeastern portion of the Bronx '
            'including Allerton, Morris Park, Van Nest, Pelham Parkway, '
            'Eastchester Gardens, and Pelham Gardens.'
        )
    elif street == 84:
        return (
            'The 84th Precinct serves a northwestern section of Brooklyn. '
            'The precinct is home to Brooklyn Heights, Boerum Hill, and Vinegar Hill.'
        )
    try:
        url = street_to_url(street)
        soup = BeautifulSoup(requests.get(url, timeout=5).text, 'html.parser')
        target_div = soup.findAll(
            "div", {"class": "span6 about-description"})[0]
        paragraphs = target_div.find_all('p')
        return paragraphs[2].text
    except:
        return "404"


def lookup(precinct):
    return pcodes[precinct]


def download_reports(args):
    reports = grab_reports(args)
    for url in reports['radio_reports']:
        df = fetch_report(url)
        download(df, url)


def merge_reports():
    data = merge()
    precincts_list = [precinct for precinct in data['Precinct'].unique()]
    desc = [extract_precinct_desc(street) for street in precincts_list]
    pcodes = {precinct: desc.strip()
              for precinct, desc in zip(precincts_list, desc)}
    data['Description'] = data['Precinct'].apply(lambda x: lookup(x))
    data.to_csv('processed.csv', index=False, encoding='utf-8')


def aggregate(data):
    new_col_names = ['Radio Runs', 'Monthly Avg', 'Lowest', 'Highest']
    monthly_aggregate = data.groupby(['Precinct'])['Radio Runs'].aggregate([
        np.sum, np.mean, np.min, np.max])
    monthly_aggregate.columns = new_col_names
    monthly_aggregate = monthly_aggregate.reset_index()
    monthly_aggregate['description'] = monthly_aggregate['Precinct'].apply(
        lambda x: lookup(x))
    monthly_aggregate.columns = [i.lower() for i in monthly_aggregate.columns]
    monthly_aggregate['precinct'] = monthly_aggregate['precinct'].astype(str)
    return monthly_aggregate


def transform(data):
    nyc_psa = gp.read_file('./data/raw/nyc_psa.geojson')
    merged = nyc_psa.merge(data, on='precinct')
    merged['rank'] = merged['radio runs'].rank(
        ascending=False, method='max').astype(int)
    merged['rank'] = merged['rank'].apply(
        lambda rank: num2words(rank, to='ordinal_num'))
    merged['analysis'] = merged.apply(lambda row: analysis(row), axis=1)
    merged['borough'] = merged['precinct'].apply(
        lambda row: infer_borough(row))
    return merged


def analysis(row):
    pre = row['precinct']
    totat_runs = row['radio runs']
    avg = np.round(row['monthly avg'], 1)
    lowest = row['lowest']
    highest = row['highest']
    rank = row['rank']
    output = (
        f"Precinct {pre} had a total of {totat_runs} radio runs between January and September. "
        f"An average of {avg} monthly radio runs with months ranging from as low as {lowest} to "
        f"high as {highest}. It ranked {rank} among 77 precincts in total radio runs for 2017."
    )
    return output


if __name__ == "__main__":
    args = get_user_args()
    download_reports(args)
    data = merge()
    data.to_csv('./data/interim/merged.csv', index=False, encoding='utf-8')
    precincts_list = [precinct for precinct in data['Precinct'].unique()]
    desc = [extract_precinct_desc(street) for street in precincts_list]
    pcodes = {precinct: desc.strip()
              for precinct, desc in zip(precincts_list, desc)}
    data = aggregate(data)
    data.to_csv('./data/processed/ipv.csv', index=False, encoding='utf-8')
    map_data = transform(data)
    map_data.to_file('./data/processed/ipv.geojson', driver="GeoJSON")
    print("Done!")
