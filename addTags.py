import os
import json, jsmin

os.chdir('Write your assets/objects path here!')
print('Begin editing furniture description files. Please wait!')

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".object"):

            with open(os.path.join(root, file)) as of:
                str = jsmin.jsmin(of.read())
                data = json.loads(str)

                try:
                    if data['category'] not in ['furniture','decorative']:
                        continue

                    tags = data['colonyTags']
                    desc = data['description']

                    wasUsed = desc.find('TAGS:')

                    if wasUsed != -1:
                        desc = desc[:(wasUsed)-1]

                    data['description'] = desc + ' TAGS: ' + ', '.join(tags)
                    print('Begin edit a file', os.path.join(root, file), '; DATA: ', data)

                except KeyError:
                    None

                with open(os.path.join(root, file), 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=2)
