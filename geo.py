pip install pystac_client
pip install planetary_computer
from pystac_client import Client
import planetary_computer as pc

# Search against the Planetary Computer STAC API
catalog = Client.open(
  "https://planetarycomputer.microsoft.com/api/stac/v1"
)

# Define your area of interest
aoi = {
  "type": "Polygon",
  "coordinates": [
    [
      [72.61883874705708, 18.847303732173202],
      [73.32779994070395, 18.847303732173202],
      [73.32779994070395, 19.26509067114233],
      [72.61883874705708, 19.26509067114233],
      [72.61883874705708, 18.847303732173202]
    ]
  ]
}

# Define your temporal range
daterange = {"interval": ["2020-01-01", "2020-12-31T23:59:59Z"]}

# Define your search with CQL2 syntax
search = catalog.search(filter_lang="cql2-json", filter={
  "op": "and",
  "args": [
    {"op": "s_intersects", "args": [{"property": "geometry"}, aoi]},
    {"op": "anyinteracts", "args": [{"property": "datetime"}, daterange]},
    {"op": "=", "args": [{"property": "collection"}, "alos-fnf-mosaic"]}
  ]
})

# Grab the first item from the search results and sign the assets
first_item = next(search.get_items())
pc.sign_item(first_item).assets
