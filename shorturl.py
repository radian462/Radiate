import requests
import os

def makeshorturl(url):
  res = requests.post('https://api.short.io/links', json={
      'domain': 'radian.f5.si',
      'originalURL': url,
    }, headers = {
          'authorization': os.getenv("shortio_API") ,
          'content-type': 'application/json'
    }, )

  res.raise_for_status()
  return(res.json()["secureShortURL"])