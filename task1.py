import requests
import exifread
from io import BytesIO

def get_image_gps(image_url):
    
    response = requests.get(image_url)
    
    
    if response.status_code != 200:
        raise Exception("Failed to download the image")
    
    
    img_file = BytesIO(response.content)
    
    
    exif_tags = exifread.process_file(img_file)
    
    
    if 'GPS GPSLongitude' not in exif_tags or 'GPS GPSLatitude' not in exif_tags:
        raise Exception("No GPS data found in the image")
    
    
    latitude = exif_tags['GPS GPSLatitude']
    longitude = exif_tags['GPS GPSLongitude']
    altitude = exif_tags.get('GPS GPSAltitude', 0) 
    
    
    lat = float(latitude.values[0]) + float(latitude.values[1])/60 + float(latitude.values[2])/float(latitude.values[3])/3600
    lon = float(longitude.values[0]) + float(longitude.values[1])/60 + float(longitude.values[2])/float(longitude.values[3])/3600
    alt = float(altitude.values[0]) / float(altitude.values[1]) if altitude else 0
    

    if str(latitude.values[3]) == 'S':
        lat = -lat
    if str(longitude.values[3]) == 'W':
        lon = -lon
    
    
    lat = round(lat, 15)
    lon = round(lon, 15)
    alt = round(alt, 15)
    
    return lon, lat, alt


image_url = "https://drive.google.com/file/d/1xPWUkLQ_wweco8nzd1BFVYjOwEBwvUff/view"
longitude, latitude, altitude = get_image_gps(image_url)
print("Longitude:", longitude)
print("Latitude:", latitude)
print("Altitude:", altitude)
