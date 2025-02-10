import csv
from lorem_text import lorem
import os

def to_name(x):
  x = x.replace(",", "_")
  x = x.replace(" ", "_")
  return x

KYSYMYKSET = []
with open("2025-02-10_vaalikoneet.csv", 'r') as infile:
  reader = csv.reader(infile, delimiter=',', quotechar='"')
  for row in reader:
    print(row)
    KYSYMYKSET += [{
      'Media': row[0],
      'Teema': row[1],
      'Kysymys': row[2]
    }]

i = 0
output_dir = "vastaukset_testi"
if not os.path.exists(output_dir):
  os.makedirs(output_dir)
for kysymys in KYSYMYKSET:
  media = to_name(kysymys['Media'])
  output_root = f'{output_dir}/{media}'
  if not os.path.exists(output_root):
    os.makedirs(output_root)
  with open(f'{output_root}/vastaus{i}.md', 'w') as outfile:
    outfile.write("+++\n")
    outfile.write(f"title = '{kysymys['Kysymys']}'\n")
    outfile.write(f"date = 2025-02-09 01:00:00\n")
    for key, val in kysymys.items():
      outfile.write(f"{key} = '{val}'\n")
    outfile.write("+++\n")
    outfile.write(f"# {kysymys['Kysymys']}\n")
    outfile.write(lorem.paragraphs(5))
    i += 1