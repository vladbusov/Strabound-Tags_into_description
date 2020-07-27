import os, httpcore
import json, jsmin
from flask import Flask, render_template
from flask_googletrans import translator
from progress.bar import FillingSquaresBar

### SETTINGS ###
objAssetsDir = 'V:\\SteamLibrary\\steamapps\\common\\Starbound\\assets\\assets\\objects'
objModeDir = 'V:\\SteamLibrary\\steamapps\\common\\Starbound\\dev\\addTags\\objects'
enableTranslating = 'ru' # translate mode to russian (place None overwise)
timeLimit = 20 # number of reruns script in case connection interrupting
### END ###

# Flask app for translation
app = Flask(__name__)
ts = translator(app)


def delEmpryDirs(path):
    for dir in os.listdir(path):
        nPath = os.path.join(path, dir)
        if os.path.isdir(nPath):
            delEmpryDirs(nPath)
            if not os.listdir(nPath):
                os.rmdir(nPath)

def countTaskLen():
    counter = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".object"):
                counter += 1
    return counter

def createModeFolder(assetsDir,modeDir):
    print('Begin editing furniture description files. Please wait!')
    os.chdir(assetsDir)
    bar = FillingSquaresBar('] Creating mode files', max=countTaskLen())

    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if not os.path.exists(modeDir + os.path.join(root,dir)[1:]):
                os.mkdir(modeDir + os.path.join(root,dir)[1:])

        for file in files:
            if file.endswith(".object"):
                bar.next()
                with open(os.path.join(root, file), encoding='utf-8') as of:
                    str = jsmin.jsmin(of.read())
                    data = json.loads(str)

                    try:
                        if data['category'] not in ['furniture','decorative']:
                            continue

                        tags = data['colonyTags']
                        desc = data['description']

                        wasUsed = max(desc.find('TAGS:'),desc.find('ТЕГИ:'))
                        if wasUsed != -1:
                            desc = desc[:(wasUsed)-1]

                        if enableTranslating:
                            # sometimes connection is interrupted
                            # this check for avoid repeated translations on script restarting
                            if os.path.isfile(modeDir + os.path.join(root ,file)[1:] + '.patch'):
                                continue

                            desc = ts.translate(text=desc, src='en', dest=[enableTranslating])

                    except KeyError:
                        continue


                    generate = json.loads('[{"value": "", "path": "/description", "op": "replace"}]')
                    generate[0]['value'] = desc + ' TAGS: ' + ', '.join(tags)

                    with open(modeDir + os.path.join(root ,file)[1:] + '.patch', 'w', encoding='utf-8') as outfile:
                        json.dump(generate, outfile, sort_keys=True, indent=2, ensure_ascii=False)

    print('\nCleaning mode folder...')
    delEmpryDirs(modeDir)



if enableTranslating:
    for _ in range(timeLimit):
        try:
            createModeFolder(objAssetsDir,objModeDir)
            print('Congratulations! Done!')
            exit()
        except httpcore._exceptions.ReadTimeout:
            print("\nConnection is interrupted! Rerun script...")
        else:
            break
else:
    createModeFolder(objAssetsDir, objModeDir)

raise httpcore._exceptions.ReadTimeout
