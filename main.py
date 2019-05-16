from keys import AZURE_API_KEY
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import json
import urllib.request
import numpy as np
import sys
import requests

def get_face_data(url):
    headers = {"Content-Type":"application/json", "Ocp-Apim-Subscription-Key": AZURE_API_KEY}
    data = {"url": url}
    faces = {}
    r = requests.post('https://eastus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=false&returnFaceLandmarks=true&returnFaceAttributes=headPose,emotion,glasses', headers=headers, data=json.dumps(data))
    faces = r.json()
    if len(faces) == 0:
        return
    if "error" in faces:
        return
    return faces

def mood(url: str=None):
    img = Image.open('output.png').convert("RGBA")
    draw_img = img.convert("RGBA")

    for f in faces:
        d = {}
        for emotion, value in f['faceAttributes']['emotion'].items():
            d[emotion] = value

        emotion = ""
        if f['faceAttributes']['glasses'] == "Sunglasses":
            emotion = "sunglasses"
        else:
            v = list(d.values())
            k = list(d.keys())
            emotion = k[v.index(max(v))]

        emojiface = Image.open('images/'+emotion+'.png').convert("RGBA")

        w, h = f['faceRectangle']['width'], f['faceRectangle']['height']
        x, y = f['faceRectangle']['left'], f['faceRectangle']['top']

        current_emojiface = emojiface.resize((w, int(w * emojiface.size[1] / emojiface.size[0])), resample=Image.LANCZOS)
        current_emojiface = current_emojiface.rotate(f['faceAttributes']['headPose']['roll'] * -1, expand=False)

        draw_img.paste(current_emojiface, (x, y), current_emojiface)

    draw_img.save('out.png')

def main(argv):
    faces = get_face_data(argv[0])
    
if __name__ == "__main__":
   main(sys.argv[1:])