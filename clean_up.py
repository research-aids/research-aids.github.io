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


#############################################
### MOVE MARKDOWN FILES TO DOCS
#############################################

MD_DIR = "./EXPORTS/WEBSITE"
DOCS_DIR = "./docs"

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


#############################################
### 
#############################################

