from collections.abc import ItemsView
import requests
import random
import re

code = ["", "-EX", "-J", "-ARC", "-JP", "-JP-J", "-JP-EX"]
weight_list = [8, 0.5, 0.5, 0.5, 5, 0.5, 0.5]
metatitle = ""
itemnumber = ""

def change_scpnumber(number):
    if number <= 99 and number > 10:
        number = f"0{number}"
    elif number < 10:
        number = f"00{number}"
    return number

def getdate():
    global metatitle
    global itemnumber
    randomnumber = random.randint(1, 7999)
    blueskyblue = random.randint(1, 8900)
    randomcode = random.choices(code, weights=weight_list)[0]

    if blueskyblue == 8900:
        randomnumber = blueskyblue  # 青い青い空(SCP-8900-EX)を例外として入れる

    randomnumber = change_scpnumber(randomnumber)
    metatitle = get_metatitle(randomnumber,randomcode)
    itemnumber = f"SCP-{randomnumber}{randomcode}"
    
    return f"http://scp-jp.wikidot.com/scp-{randomnumber}{randomcode}"

def get_metatitle(number, code):
  metatitle = ""
  minicode = ""

  if code == "-EX":
    url = "http://scp-jp.wikidot.com/scp-ex"
  elif code == "-J":
    url = "http://scp-jp.wikidot.com/joke-scps"
  elif code == "-ARC":
    url = "http://scp-jp.wikidot.com/archived-scps"
  elif code == "-JP-EX":
    url = "http://scp-jp.wikidot.com/scp-jp-ex"
  elif code == "-JP-J":
    url = "http://scp-jp.wikidot.com/joke-scps-jp"

  if number < 1000:
    url = f"http://scp-jp.wikidot.com/scp-series{code}"
  else:
    tipnumber = number//1000 + 1
    url = f"http://scp-jp.wikidot.com/scp-series{code}-{tipnumber}"

  number = change_scpnumber(number)

  if code == "-JP":
    minicode = "-jp"
  elif code == "-EX":
    minicode= "-ex"
  elif code == "-J":
    minicode= "j"
  elif code == "-ARC":
    minicode= "-arc"
  elif code == "-JP-EX":
    minicode= "-jp-ex"
  elif code == "-JP-J":
    minicode= "-j-jp"

  response = requests.get(url)
  match = re.search(fr'<li><a href="/scp-{number}{minicode}">SCP-{number}{code}</a>(.+)</li>', response.text)
  if match:
    metatitle = match.group(1)
    return metatitle

def randomscp():
  url = getdate()

  while requests.get(url).status_code == 404:
    url = getdate()

  return f"{itemnumber} {metatitle}\n{url}"
