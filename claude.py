import anthropic
import math
import time
import csv
import os
import sys
import yaml

with open('creds.yml', 'r') as cfgfile:
  creds = yaml.load(cfgfile)
ajokerta = sys.argv[1]

APIKEY = creds['claude_token']

OHJELMAT = {
    "ohjelmat/poliittinenohjelma.txt": "Vihreiden poliittinen ohjelma.",
    "ohjelmat/soteohjelma.txt": "Vihreiden sosiaali- ja terveysohjelma.",
    "ohjelmat/kaupunkitavoitteet.txt": "Vihreiden tavoitteet suurille kaupungeille",
    "ohjelmat/maaseutuohjelma.txt": "Vihreiden alue- ja maaseutuohjelma"
}

QUESTIONPROMPT = """Kysymys on "{kysymys}". Miten vastaat?"""

client = anthropic.Anthropic(api_key = APIKEY)
MODEL_NAME = "claude-3-5-sonnet-20241022"

SYSTEM = [
    {
        "type": "text",
        "text": "Olet vihreä kuntavaaliehdokas. Olet vastaamassa vaalikoneeseen. Vastauksen tulee hyödyntää mahdollisimman paljon aiemmin annettuja Vihreiden ohjelmia. Mitkä ovat tärkeimmät vastauksessa mainittavat asiat? Käytä ranskalaisia viivoja."
    }
]

for filename, description in OHJELMAT.items():
    with open(filename, 'r') as infile:
        file_contents = infile.read()
        SYSTEM += [{
            "type": "text",
            "text": f"Alla {description}. {file_contents}",
            "cache_control": {"type": "ephemeral"}
        }]

def to_name(x):
  x = x.replace(",", "_")
  x = x.replace(" ", "_")
  return x

KYSYMYKSET = []
with open("2025-02-10_vaalikoneet.csv", 'r') as infile:
  reader = csv.reader(infile, delimiter=',', quotechar='"')
  for row in reader:
    KYSYMYKSET += [{
      'Media': row[0],
      'Teema': row[1],
      'Kysymys': row[2]
    }]

i = 0
output_dir = f"vastaukset_{ajokerta}"
if not os.path.exists(output_dir):
  os.makedirs(output_dir)
for kysymys in KYSYMYKSET:
  media = to_name(kysymys['Media'])
  output_root = f'{output_dir}/{media}'
  if not os.path.exists(output_root):
    os.makedirs(output_root)
  print(kysymys)
  this_msg = {
     "role": "user",
     "content": f"Kysymys on {kysymys['Kysymys']}. Miten vastaat?"
  }
  vastaus_filename = f'{output_root}/vastaus{i}.md'
  if os.path.exists(vastaus_filename):
    print("Tehty jo, ohitetaan.")
  else:
    res = client.messages.create(
      model = MODEL_NAME,
      max_tokens = 1024,
      messages = [this_msg])
    vastaus = res.content[0].text
    print(vastaus)
    with open(vastaus_filename, 'w') as outfile:
      outfile.write("+++\n")
      outfile.write(f"title = '{kysymys['Kysymys']}'\n")
      outfile.write(f"date = 2025-02-09 01:00:00\n")
      for key, val in kysymys.items():
          outfile.write(f"{key} = '{val}'\n")
      outfile.write("+++\n")
      outfile.write(f"# {kysymys['Kysymys']}\n")
      outfile.write(vastaus)
    time.sleep(3)
  i += 1
  