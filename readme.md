# Create Map Posters

If you've ever seen all over Etsy and other websites, you can buy custom posters that highlight a map of a certain location. After seeing the sometimes outrageous prices of these incredibly simple posters, I created my own script to automate creating these. I got these printed at a nearby print shop to create some cheap easy decor for my home that feels personalized and meaningful. See some examples below!

## Usage

1. Modify the `cities.json` to include the coordinates and info for the locations you want to create posters of. Make sure you keep it colocated with the script.
2. Just run `createMap.py`. The posters should all appear in the directory named `posters` in less than a minute.

## Specifications

I used Python 3.8 to run this script. The list of Python modules used is:

* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Html2Image](https://pypi.org/project/html2image/)
* [Folium](https://python-visualization.github.io/folium/)

## Formatting Your Cities JSON

The JSON used to specify the list of cities/locations should be pretty straightforward. I've included an example JSON too. If anything's unclear, for each city you just need to include:

* **name:** the name of the city which will become the large text title
* **country:** the country of the city which will become the smaller text subtitle
* **lat:** the latitude you want the map to be centered on
* **lon:** the longitude you want the map to be centered on
* **zoom start:** an integer 0-18 which determines how zoomed the map should be. This also changes how detailed the map is with features such as roads. If you want to zoom in/out without changing how detailed the map is or want a zoom between two integers I suggest modifying the `zoom_mult` variable in the script in conjunction with this argument to get your desired result.

