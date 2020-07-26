import os
import json, jsmin

os.chdir('V:\\SteamLibrary\\steamapps\\common\\Starbound\\assets\\assets\\objects')
print('Begin editing furniture description files. Please wait!')

modeDir = 'V:\\SteamLibrary\\steamapps\\common\\Starbound\\dev\\addTags\\objects'


def delEmpryDirs(path):
    for dir in os.listdir(path):
        nPath = os.path.join(path, dir)
        if os.path.isdir(nPath):
            delEmpryDirs(nPath)
            if not os.listdir(nPath):
                os.rmdir(nPath)

for root, dirs, files in os.walk("."):
    for dir in dirs:
        if not os.path.exists(modeDir + os.path.join(root,dir)[1:]):
            os.mkdir(modeDir + os.path.join(root,dir)[1:])

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
                    # print('New: ', modeDir + os.path.join(root ,file)[1:], dirs)

                except KeyError:
                    None


                with open(modeDir + os.path.join(root ,file)[1:], 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=2)

delEmpryDirs(modeDir)