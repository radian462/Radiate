import requests
import random
import re
import json
import os

def make_database():
  with open("function_file/scp_date.json", "r+") as f:
    f.truncate(0)

  def filter_lines(input_text):
      lines = input_text.split('\n')
      filtered_lines = [line for line in lines if re.search(r'<li><a href="/scp-', line) and "scp-ex" not in line or re.search(r'<li><a href="/scpaaaaaaaaaaaaaaaaaa-jp-j', line) or re.search(r'<span class="taboo">', line)]
      filtered_lines = [re.sub('<span class="taboo">', "", line) for line in filtered_lines]
      result_text = '\n'.join(filtered_lines)
      return result_text

  url_list = ["scp-series","scp-series-2","scp-series-3","scp-series-4","scp-series-5","scp-series-6","scp-series-7","scp-series-8",
              "joke-scps","archived-scps","scp-ex","scp-series-jp","scp-series-jp-2","scp-series-jp-3","scp-series-jp-4",
              "joke-scps-jp","archived-scps-jp","scp-jp-ex"]

  scp_data = {}

  for url in url_list:
      response = requests.get(f"http://scp-jp.wikidot.com/{url}")
      scp_dates = '\n'.join(re.findall(r'<ul>(.*?)</ul>', response.text, re.DOTALL))
      filtered_text = filter_lines(scp_dates)

      with open("function_file/scp_date.html", "w", encoding="utf-8") as f:
          f.write(filtered_text)

      with open("function_file/scp_date.html", encoding="utf-8") as f:
          for line in f:
              if '<a class="newpage"' not in line:
                  scp_id = re.search(r'<li><a href="/(.+?)">', line)
                  if not re.match(r'scp-\d+', scp_id.group(1)):
                      scp_id = re.search(fr'<a href="/{scp_id.group(1)}">(.+?)</a>', line)

                  itemnumber = re.search(fr'">(.+?)</a>', line)
                  metatitle = re.search(r'</a>(.+)</li>', line)
                  if scp_id and itemnumber and metatitle:
                      scp_data[scp_id.group(1)] = [itemnumber.group(1), metatitle.group(1)]

      os.remove('function_file/scp_date.html')

  with open("function_file/scp_date.json", mode="w", encoding="utf-8") as f:
      json.dump(scp_data, f, ensure_ascii=False, indent=2)
  print("SCPデータを収集しました")

def random_scp():
  with open('function_file/scp_date.json', 'r') as file:
    scp_database = json.load(file)
    scp_id = random.choice(list(scp_database.keys()))
    itemnumber = scp_database[scp_id][0]
    metatitle = scp_database[scp_id][1]

    metatitle = re.sub(r'&quot;', '"', metatitle)
    metatitle = re.sub(r'<strong>|</strong>', '**', metatitle)
    metatitle = re.sub(r'<span class="rt">(.*?)</span>', r'(\1)', metatitle)
    metatitle = re.sub(r'<span style="text-decoration: line-through;">(.*?)</span>', r'~~\1~~', metatitle)
    metatitle = re.sub(r'<(.*?)>', '', metatitle)

  return f"{itemnumber}{metatitle}\nhttp://scp-jp.wikidot.com/{scp_id}"
