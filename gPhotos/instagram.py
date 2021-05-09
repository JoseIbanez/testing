from instabot import Bot 
from PIL import Image
import sys
from config import getConfig

def upload(input_image):

    image = Image.open(f"/tmp/{input_image}")

    # get lower dimmension
    print(f"Origina size: {image.size}")

    w, h = image.size

    if w < h:
        s = w
    else:
        s = h

    box = (int(w/2 - s/2), int(h/2 - s/2), int(w/2 + s/2), int(h/2 + s/2))
    print(f"Crop box: {box}")

    cropped_image = image.crop(box)
    cropped_image.save('/tmp/cropped_image.jpg')


    # Login to Instagram
    bot = Bot() 
    bot.login(username=getConfig('instagram.username')) 


    # Upload
    bot.upload_photo("/tmp/cropped_image.jpg",  caption ="") 


if __name__ == '__main__':

    upload(sys.argv[1])

