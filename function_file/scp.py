import requests
import random
import re

def change_itemnumber(number):
  if number <= 99 and number > 10:
    number = f"0{number}"
  elif number < 10:
    number = f"00{number}"
  return number

def get_scpdate():
  scp_codes = ["", "-EX", "-J", "-ARC", "-JP", "-JP-J", "-JP-EX"]
  weight_list = [8, 0.5, 0.5, 0.5, 5, 0.5, 0.5]

  while True:
      number = random.randint(1, 7999)
      blueskyblue = random.randint(1, 8900)
      chosen_code = random.choices(scp_codes, weights=weight_list)[0]
      url = f"http://scp-jp.wikidot.com/scp-{number}{chosen_code}"

      if blueskyblue == 8900:#青い青い空を例外指定
          number = blueskyblue

      if requests.get(url).status_code != 404:
          return number, chosen_code, url

def get_metatitle(itemnumber,code):
  #オブジェクトクラス取得先決定
  if code == "" or code == "-JP":
    if itemnumber < 1000:
      url = f"http://scp-jp.wikidot.com/scp-series{code}"
    else:
      tipnumber = itemnumber//1000 + 1
      url = f"http://scp-jp.wikidot.com/scp-series{code}-{tipnumber}"  
  elif code == "-EX" or code == "-JP-EX":
    url = f"http://scp-jp.wikidot.com/scp{code}"
  elif code == "-J":
    url = "http://scp-jp.wikidot.com/joke-scps"
  elif code == "-ARC":
    url = "http://scp-jp.wikidot.com/archived-scps"
  elif code == "-JP-J":
    url = "http://scp-jp.wikidot.com/joke-scps-jp"

  minicode = code.lower()
  itemnumber = change_itemnumber(itemnumber)

  response = requests.get(url)
  match = re.search(fr'<li><a href="/scp-{itemnumber}{minicode}">SCP-{itemnumber}{code}</a>(.+)</li>',response.text)
  if match:
    metatitle = match.group(1)
    return metatitle

def randomscp():
  scpdate = get_scpdate()
  itemnumber = change_itemnumber(scpdate[0])
  return f"SCP-{itemnumber}{scpdate[1]}{get_metatitle(scpdate[0],scpdate[1])}\n{(scpdate[2])}"

