import re

import geopy
from geopy.geocoders import Nominatim

import matplotlib.pyplot as plt
import matplotlib.cm

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

import pandas

CSV_FILE = '2017-09-04_rent.csv'

geolocator = Nominatim()


def load_data():
    pd = pandas.read_csv(CSV_FILE)
    pd = pd[['price', 'city']]

    gb = pd.groupby(by='city').mean().round()

    print(gb.head())
    print(len(gb), 'unique cities')

    s = gb.stack()

    print(s[['Metz', 'Nancy', 'Paris', 'Strasbourg']])

    for city, price in gb.iterrows():
        pass


def geolocate(data):
    location = geolocator.geocode("23 rue st hubert, hambach, france")
    print(location.address, (location.latitude, location.longitude))
    zipcode = parse_zipcode(location.address)
    geoloc = (zipcode, location.latitude, location.longitude)
    return geoloc


def parse_zipcode(address):
    def build_zipcode_regex():
        """Build a regex that matches the zipcode in address string."""
        # Regex scanf-like building blocks
        r_zip = r'\d+'
        r_prog = re.compile(r_zip)
        return r_prog

    r_prog = build_zipcode_regex()

    re_res = r_prog.match(address)
    matched = re_res is not None
    if matched:
        return re_res.string


def plot_map():
    fig, ax = plt.subplots(figsize=(10, 20))

    # France:
    # westlimit=-5.08; southlimit=42.11;
    #  eastlimit=8.57; northlimit=51.23

    m = Basemap(resolution='l',  # c, l, i, h, f or None
                projection='merc',
                lat_0=54.5, lon_0=-4.36,
                llcrnrlon=-5.08, llcrnrlat=42.11,
                urcrnrlon=8.57, urcrnrlat=51.23)

    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
    m.drawcoastlines()

def main():
    data = load_data()

    geolocate(data)
    # data['geoloc'] = geolocate(data)

    plot_map()
    plt.show()

# if __name__ == '__main__':
    # main()
