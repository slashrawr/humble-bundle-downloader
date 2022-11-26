import os
import requests
import json
from tqdm import tqdm

key = ""
download_path = ""
chunk_size = 4096
cookie_jar = {
    "_simpleauth_sess": ""
}

response = requests.request(
    method="GET",
    url="https://www.humblebundle.com/api/v1/order/" + key,
    cookies=cookie_jar
)

raw = json.loads(response.content)

order_name = raw["product"]["human_name"]
number_of_downloads = len(raw["subproducts"])

overall_progress = tqdm(total=number_of_downloads, unit="files", unit_scale=True, desc="Overall", colour="magenta", position=1)

for subproducts in raw["subproducts"]:
    name = subproducts["machine_name"]
    for downloads in subproducts["downloads"]:
        dlstruct = downloads["download_struct"][0]
        url = dlstruct["url"]["web"]
        file_size = dlstruct["file_size"]
        
        filename = download_path + name + ".zip"
        
        if (os.path.isfile(filename) == False):
            progress_bar = tqdm(total=file_size, unit="iB", unit_scale=True, desc=name, colour="cyan", position=0)
            with requests.get(url, stream=True) as r:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size): 
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))

        else:
            print("Already exists: ", name)
        
        progress_bar.close()
        overall_progress.update(1)

overall_progress.close()