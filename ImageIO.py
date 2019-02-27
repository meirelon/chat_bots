import requests
from PIL import Image
from io import BytesIO

def get_image(url):
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    img.save("/tmp/photo.jpg")


def get_vision_request(key, bucket_path):
    vision_api = "https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=key)
    remote_request_json = {
      "requests": [
        {
          "image": {
            "source": {
              "imageUri": "https://storage.googleapis.com/" + bucket_path + "/photo.jpg"
            }
          },
          "features": [
            {
                "type" : "FACE_DETECTION",
                "maxResults" : 1
            }
          ]
        }
      ]
    }
    return requests.post(url=vision_api, json=remote_request_json)

def get_emotion(r):
    emotions = ["joy", "anger", "sorrow", "surprise"]
    emotion_likelihoods = [r.json().get("responses")[0].get("faceAnnotations")[0].get("{emotion}Likelihood".format(emotion=emotion)) for emotion in emotions]
    emotion_dictionary = dict(zip(emotions, emotion_likelihoods))
    for k,v in emotion_dictionary.items():
        emotion_list = []
        if v in (["VERY_LIKELY","LIKELY", "POSSIBLE"]):
            emotion_list.append(k)
        if len(emotion_list) > 0:
            return emotion_list[0]
        else:
            return "neutral"
