import glob
import sys
import os
import toml
import re

TARGET_TAGS = [
    'Aluevaalit', 'Arvot', 'Asuminen', 'Kasvatus ja koulutus',
    'Koulut', 'Kulttuuri', 'Kuntavaalit', 'Liikenne', 'Maahanmuutto',
    'Talous', 'Väestö ja asuminen', 'Ympäristö'
    ]

MEDIA = {
    'HS__AL': 'HS, Aamulehti, Suomen Kuvalehti',
    'HS__AL__SK': 'HS, Aamulehti, Suomen Kuvalehti',
    'IL': 'Iltalehti',
    'IS': 'Ilta-Sanomat'
}

source_dir = sys.argv[1]
target_file = sys.argv[2]

def parse_frontmatter(fp):
    in_fm = False
    content = ""
    frontmatter_str = ""
    for row in fp:
        if row == '+++\n':
            if in_fm:
                frontmatter = toml.loads(frontmatter_str)
                in_fm = False
            else:
                in_fm = True
        else:
            if in_fm:
                frontmatter_str += row
            else:
                content += row
    return (frontmatter, content)

with open(target_file, 'w') as outfile:  
    for this_dir in glob.glob(f"{source_dir}/*"):
        this_media = MEDIA[os.path.split(this_dir)[1]]
        outfile.write(f"# {this_media}\n\n")
        for this_file in glob.glob(f"{this_dir}/*.md"):
            with open(this_file, 'r') as infile:
                frontmatter, content = parse_frontmatter(infile)
            is_target = False
            for t in frontmatter['tags']:
                if t in TARGET_TAGS:
                    is_target = True
            if is_target:
                outfile.write(f"## {frontmatter['Kysymys']}\n\n")
                outfile.write(f"Teemat: {",".join(frontmatter['tags'])}\n\n")
                outfile.write(content)
                outfile.write("\n\n")
            else:
                print(f"{frontmatter['tags']} not in TARGET_TAGS, skipping...")
