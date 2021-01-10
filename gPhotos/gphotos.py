import io
import base64
#from tkinter import *
from urllib.request import urlopen
from gphotospy import authorize
from gphotospy.media import *
from gphotospy.album import *
import urllib.request
import random
from PIL import Image
from config import getConfig


# https://dev.to/davidedelpapa/manage-your-google-photo-account-with-python-p-1-9m2


def download():

    # Select secrets file
    CLIENT_SECRET_FILE = "gphoto_oauth.json"

    # Get authorization and return a service object
    service = authorize.init(CLIENT_SECRET_FILE)

    # Construct the album manager
    album_manager = Album(service)

    # Get iterator over the list of albums
    album_iterator = album_manager.list()


    title = None
    targetAlbum = getConfig('gphotos.album')
    while title != targetAlbum:

        # Let's get the next album in the list
        first_album = next(album_iterator)
        title =first_album.get("title")
        print(title)


    # Let's get this album's id
    first_album_id = first_album.get("id")


    # Construct the media manager
    media_manager = Media(service)

    # Let's get a list of all the album's content
    album_media_list = list(media_manager.search_album(first_album_id))

    album_len = len(album_media_list)

    #for idx,item in enumerate(album_media_list):
    #    #print(f"item:{item}")
    #    print(f"idx:{idx}, mimeType:{item.get('mimeType')} filename:{item.get('filename')}")



    index = random.randrange(album_len)


    # Let's get the baseUrl of the first item
    base_url = album_media_list[index].get("baseUrl")
    filename = album_media_list[index].get("filename")

    # Let's format the baseUrl with parameters
    # and prepare it for display within the Canvas
    image_url = "{}=w1200-h1200".format(base_url)

    #print(image_url)

    #image_bytes = urlopen(image_url).read()


    urllib.request.urlretrieve(image_url, f"/tmp/{filename}")
    print(f"filename: {filename}")

    return filename

if __name__ == '__main__':

    download()

