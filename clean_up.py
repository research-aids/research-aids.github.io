from glob import glob
import yaml
import json
import re

import os
from pathlib import Path
import shutil


#############################################
### REMOVE UNCESSARY FILES FROM PARENT
#############################################

try:
    Path.unlink("directory_tree.md")
    Path.unlink("README.md")
    Path.unlink("handbook.md")

    shutil.rmtree("forKinsukAndSjors")
    shutil.rmtree("offline")
    # shutil.rmtree("review")

except FileNotFoundError:
    print("seems like files were already gone...")


try:
    Path.unlink("./github/workflows/check_yaml.yml")
    Path.unlink("./github/workflows/yaml2json.yml")
    Path.unlink("./github/workflows/yaml_export.yaml")
except FileNotFoundError:
    print("phew, workflow files already gone")


#############################################
### MOVE MARKDOWN FILES TO DOCS
#############################################

def copy_to_docs(MD_DIR, DOCS_DIR):
    # os.makedirs(DOCS_DIR)
    niveau_files = glob(MD_DIR + "/*/*.md")
    for f in niveau_files:
        # with open(f) as handle:
        dest_fpath = f.replace(MD_DIR, DOCS_DIR)
        print(f"copying {f} to {dest_fpath}")
    
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copy2(f, dest_fpath)
    
    
    
    md_files = glob(MD_DIR + "/*/Dutch/*.md") + glob(MD_DIR + "/*/English/*.md")
    
    for f in md_files:
        # with open(f) as handle:
        dest_fpath = f.replace(MD_DIR, DOCS_DIR)
        print(f"copying {f} to {dest_fpath}")
    
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copy2(f, dest_fpath)

copy_to_docs("./EXPORTS/WEBSITE/published", "./docs/published")
copy_to_docs("./EXPORTS/WEBSITE/review", "./docs/review")

#############################################
### ADD DATE TO INDEX.HTML
#############################################

# print(glob("*"))
# print(glob(DOCS_DIR+"/*"))

DOCS_DIR = "./docs"

from datetime import datetime
index = ""
with open(DOCS_DIR + "/index.md", "r") as handle:
    index += handle.read()

with open(DOCS_DIR + "/index.md", "w") as handle:
    index += "\n\n" + f"current version from {datetime.now()}"#.strftime("%Y-%m-%d")}"

    handle.write(index)