import json
from datetime import datetime


with open('./list.json') as f:
    patch_list = json.load(f)['data']

with open('./list.csv', 'w') as f:
    for item in patch_list:
        description = item['description']
        patch_name = item['productPatchName']
        patch_version = item['productPatchVersion']
        patch_time_timestamp = str(item['addTime'])[:10]
        patch_time = datetime.fromtimestamp(int(patch_time_timestamp))
        patch_status = item['status']

        if patch_status == 1:
            f.write("{}${}${}${}\n".format(description, patch_name, patch_version, patch_time))