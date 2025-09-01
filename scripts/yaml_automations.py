from tqdm import tqdm
import yaml
from glob import glob
import os

from datetime import datetime

os.chdir("..")



BASE_DIR = "./published"

if not os.path.isdir(BASE_DIR):
    print("not sure where I am, exiting!")
    exit()
    
eng = glob(f"{BASE_DIR}/*/English/*.yml")
dutch = glob(f"{BASE_DIR}/*/Dutch/*.yml")
# top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = dutch + eng

license_dict = dict(
  license="https://creativecommons.org/licenses/by-sa/4.0/deed.en",
  copyright_holder="NIOD-KNAW",
  date=datetime.today().strftime("%Y-%m-%d")
)
        

for f in tqdm(yaml_files):
    print(f"processing {f}...")
    with open(f) as handle:
        yaml_content = yaml.safe_load(handle)
        if not yaml_content: print("---", f, yaml_content)
        yaml_content["copyright_metadata"] = license_dict

        print(type(yaml_content), yaml_content["copyright_metadata"])
    with open(f, "w") as handle:
        yaml.dump(yaml_content, handle)
        
