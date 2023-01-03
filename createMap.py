import folium
import time
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from html2image import Html2Image

# Constants

POSTER_WIDTH = 1650
POSTER_HEIGHT = 2550
POSTER_SIZE = (POSTER_WIDTH, POSTER_HEIGHT)
STYLE = 'CartoDBPositron'

# Globals

modern_mask = None
hti = Html2Image(output_path='screenshots', custom_flags=['--virtual-time-budget=10000'])

# Read cities JSON to create posters from

def loadCities():
    f = open('cities.json',)
    data = json.load(f)
    f.close()
    return data['cities']

# Helpers

def mapFilenameOfCity(city):
    folder_name = 'htmls'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    return folder_name + '/' + city["name"] + '.html'

def screenshotInitialFilenameOfCity(city):
    return city["name"] + '.png'

def screenshotFilenameOfCity(city):
    folder_name = 'screenshots'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    return folder_name + '/' + city["name"] + '.png'

def posterFilenameOfCity(city):
    folder_name = 'screenshots'
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    return folder_name + '/' + city["name"] + '.png'

def tilesForStyle(style):
    if style == 'StamenToner':
        return "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png"
    elif style == 'CartoDBPositron':
        return "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
    return None

def shouldDarken(style):
    return style == 'CartoDBPositron'

# Creating the map image

def createScreenshot(city):
    # Create the HTML map
    coordinates = [city["lat"], city["lon"]]
    zoom_start = int(city["zoom start"])
    m = folium.Map(location=coordinates, tiles=tilesForStyle(STYLE), zoom_start=zoom_start, attr="_")
    html_file = mapFilenameOfCity(city)
    m.save(html_file)
    hti.screenshot(
        html_file=html_file,
        save_as=screenshotInitialFilenameOfCity(city)
    )

# Creating the poster

def createModernPoster(city):
    # Local constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_NAME = "Futura.ttc"
    FOOTER_HEIGHT = 400
    FADE_HEIGHT = 600
    TOP_OF_TEXT = 1950 + 60
    BORDER_WIDTH = 50
    # Start the poster
    poster = Image.new('RGBA', POSTER_SIZE, color='white')
    draw = ImageDraw.Draw(poster, 'RGBA')
    # Paste the map image in the center
    mapImage = ImageOps.grayscale(Image.open(screenshotFilenameOfCity(city)))
    originalMapWidth, originalMapHeight = mapImage.size
    newMapWidth = int(originalMapWidth * POSTER_HEIGHT / originalMapHeight)
    zoom_multiplier = 1.5
    mapImage = mapImage.resize((int(newMapWidth * zoom_multiplier), int(POSTER_HEIGHT * zoom_multiplier)))
    if shouldDarken(STYLE):
        darken = lambda p: 0.9 * p * p * p / 255 / 255
        mapImage = mapImage.point(darken)
    newMapWidth, newMapHeight = mapImage.size
    pasteX = int((POSTER_WIDTH - newMapWidth) / 2)
    pasteY = int((POSTER_HEIGHT - newMapHeight) / 2)
    poster.paste(mapImage, (pasteX, pasteY))
    # Add white border
    borderBoundingBox = [(0,0), (POSTER_WIDTH, POSTER_HEIGHT)]
    draw.rectangle(borderBoundingBox, fill=None, outline=WHITE, width=BORDER_WIDTH)
    # Add white footer and fade
    bottomOfFade = POSTER_HEIGHT - FOOTER_HEIGHT
    topOfFade = bottomOfFade - FADE_HEIGHT
    fadeLayer = Image.new('RGBA', POSTER_SIZE, color=None)
    fadeDraw = ImageDraw.Draw(fadeLayer, 'RGBA')
    for y in range(topOfFade, POSTER_HEIGHT):
        endpoints = [(0, y), (POSTER_WIDTH, y)]
        opacity = int(255 * (y - topOfFade) / (bottomOfFade - topOfFade))
        opacity = max(0, min(opacity, 255))
        fadingWhite = (255, 255, 255, opacity)
        fadeDraw.rectangle(endpoints, fill=None, outline=fadingWhite, width=1)
    poster = Image.alpha_composite(poster, fadeLayer)
    draw = ImageDraw.Draw(poster, 'RGBA')
    # Add city name
    font = ImageFont.truetype(FONT_NAME, 150)
    text = city['name'].upper()
    textWidth, textHeight = draw.textsize(text, font)
    location = int((POSTER_WIDTH - textWidth) / 2), TOP_OF_TEXT
    draw.text(location, text, BLACK, font=font)
    # Add country name
    font = ImageFont.truetype(FONT_NAME, 90)
    text = city['country'].upper()
    textWidth, textHeight = draw.textsize(text, font)
    location = int((POSTER_WIDTH - textWidth) / 2), TOP_OF_TEXT + 200
    draw.text(location, text, BLACK, font=font)
    # Add coordinates
    font = ImageFont.truetype(FONT_NAME, 65)
    lat, lon = float(city['lat']), float(city['lon'])
    northSouth = 'N' if lat > 0 else 'N'
    eastWest = 'W' if lon < 0 else 'E'
    latText = "{:.2f}".format(abs(lat))
    lonText = "{:.2f}".format(abs(lon))
    text = '{0}° {1}, {2}° {3}'.format(latText, northSouth, lonText, eastWest)
    textWidth, textHeight = draw.textsize(text, font)
    location = int((POSTER_WIDTH - textWidth) / 2), TOP_OF_TEXT + 350
    draw.text(location, text, BLACK, font=font)
    # Save the poster
    poster.save(posterFilenameOfCity(city), "png")

#
#       MAIN
#

def main():

    # Arguments

    # use-temp-files, defaults to true
    # output-directory, defaults to posters in current directory
    # style, defaults to CartoDBPositron
    # cities-file, defaults to cities.json

    cities = loadCities()
    for city in cities:
        createScreenshot(city)
        createModernPoster(city)

if __name__ == "__main__":
    main()
