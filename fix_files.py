import glob
import sys
import os
import toml
import re

source_dir = sys.argv[1]
target_dir = sys.argv[2]

for filename in glob.glob(f"{source_dir}/*/*.md"):
    print(filename)
    with open(filename, 'r') as infile:
        in_fm = False
        content_str = ""
        frontmatter_str = ""
        for row in infile:
            if row == '+++\n':
                if in_fm:
                    print(frontmatter_str)
                    frontmatter = toml.loads(frontmatter_str)
                    in_fm = False
                else:
                    in_fm = True
            else:
                if in_fm:
                    frontmatter_str += row
                else:
                    content_str += row
    frontmatter['tags'] = [frontmatter['Teema']]
    frontmatter['category'] = [frontmatter['Media']]
    print(content_str)
    content_str = re.sub(r"# .*", "", content_str)
    print(content_str)
    for subdir in glob.glob(f"{source_dir}/*"):
        new_subdir = subdir.replace(source_dir, target_dir)
        if not os.path.exists(new_subdir):
            os.makedirs(new_subdir)
    with open(filename.replace(source_dir, target_dir), 'w') as outfile:
        outfile.write("+++\n")
        outfile.write(toml.dumps(frontmatter))
        outfile.write("+++\n")
        outfile.write(content_str)
