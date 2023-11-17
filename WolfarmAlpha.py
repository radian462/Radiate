import wolframalpha
import os

client = wolframalpha.Client(os.getenv("wolframalpha_api"))

def calc(request): 
  global text
  res = client.query(request)
  os.remove('WolframAlpha.txt')
  for pod in res.pods:
    for sub in pod.subpods:
      if sub.plaintext:
        with open("WolframAlpha.txt", "a") as o:
          print(sub.plaintext, file=o)
        with open("WolframAlpha.txt", 'r') as o:
          text = o.read()
  
  return(text)

  
        


        
