import os
import subprocess
import uuid
import json
import time
from flask import Flask, request, render_template, url_for, redirect
from flask_table import Table, Col
import numpy as np
import azure.cosmos.cosmos_client as cosmos_client
from shutil import copyfile
import shutil


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'C:/Users/funpa/OneDrive/Desktop/nux'

#config = {
#    'ENDPOINT': 'https://9928c7b3-0ee0-4-231-b9ee.documents.azure.com:443/',
#    'PRIMARYKEY': 'Z1Cu587FxkqD9T5yCIVPQQATZ2BmVEJ3GLsKs6SvqhAW9F5W9GgLba8mJXhMIlg4AF3obFaSOFybjlqxYDk3Nw==',
#    'DATABASE': 'CosmosDatabase',
#    'CONTAINER': 'CosmosContainer'
#}

#client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})
#database_link = 'dbs/CosmosDatabase'
#database = client.ReadDatabase(database_link)

#id = 'CosmosContainer'
#collection_link = database_link + '/colls/{0}'.format(id)
#userContainer = client.ReadContainer(collection_link)

@app.route("/")
def fileFrontPage():
    return render_template('homepage.html')

@app.route("/retrievePass", methods=["POST"])
def retrievePass():
    userName = request.form['getpassfromUser']

    find_entity_by_id_query = {
    "query": "SELECT * FROM CosmosContainer c where c.id = @id",
    "parameters": [
            { "name":"@id", "value": str(userName) }
        ]
    }

    options = {}
    options['enableCrossPartitionQuery'] = True

    entities = None
    entities = list(client.QueryItems(collection_link, find_entity_by_id_query, options))
    tempDict = entities[0]
    print(tempDict['Password'])

    return redirect(url_for('fileFrontPage'))

@app.route("/upload", methods=["GET", "POST"])
def fileUploadPage():
    return render_template('features.html')

@app.route("/handleID", methods=["GET", "POST"])
def storeUser():
    userID = request.form['userID']
    password = request.form['password']
    client.CreateItem(userContainer['_self'], {
        'id': userID,
        'Total Runs': 0,
        'Password': password,
        'FolderID': str(uuid.uuiud4())
        }
    )
    return redirect(url_for('fileFrontPage'))

@app.route("/arrayDisplay", methods=["GET", "POST"])
def displayArrayInfo():
    return render_template('displayData.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    threshold = 9
    
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':      
            uniqID = uuid.uuid4()
            os.mkdir(str(uniqID))
            os.mkdir(os.path.join(str(uniqID), 'labeled'))
            shutil.copy('BranchLogger.class', os.path.join(str(uniqID), 'labeled'))
            photo.save(os.path.join('C:/Users/funpa/OneDrive/Desktop/nux', str(uniqID), photo.filename))
            subprocess.Popen(['initate.bat', str(uniqID), photo.filename, os.path.join(str(uniqID), 'labeled', 'BranchLogger.class')], shell=True)
            filePresent = True

            arrayData = []
            while filePresent:
                try:
                    with open(os.path.join(str(uniqID), str(threshold) + '_tendydemei.json')) as thefile:
                        arrayData = json.load(thefile)
                    filePresent = False
                except:
                    continue

            filePresent = True
            temp = []    
            randomints = []
            bitmaps = []

            for bitvals in arrayData.values(): temp.append(bitvals)
            
            i = 0
            for rows in temp: 
                randomints.append(temp[i][0]) 
                bitmaps.append(temp[i][1]) 
                i += 1
            q = 0
            for val in bitmaps:
                bitmaps[q] = np.sum(val)
                q+=1
            
            fullVals = [0] * len(bitmaps)
            z = 0
            for array in randomints:
                fullVals[z] = np.append(array, bitmaps[z])
                z += 1


            return render_template('displayData.html', arrayInts = fullVals)
            

if __name__ == '__main__':
    app.run(debug=True)  