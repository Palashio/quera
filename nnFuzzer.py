import innvestigate
from innvestigate.analyzer import BaselineGradient
from innvestigate.analyzer import Gradient
import os
import sys
import json
import numpy as np
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from sklearn.model_selection import train_test_split

folderID = sys.argv[1]
iterID = 0
javaFile = False
dictID = 0

for x in range(10):
    while(not javaFile):
        try:       
            with open(os.path.join(str(folderID), str(iterID) + '_demei.json')) as json_file:  
                data = json.load(json_file)
                print(str(iterID) + " iteration picked up")
                javaFile = not javaFile
        except:
            continue

    javaFile = False
    print('point reached')      
    temp = []    
    randomints = []
    bitmaps = []


    for bitvals in data.values(): temp.append(bitvals)

    i = 0
    for rows in temp: 
        randomints.append(temp[i][0]) 
        bitmaps.append(temp[i][1]) 
        i += 1

    listofBoth = [randomints, bitmaps]
    sums = np.sum(listofBoth[1], axis=0)
    counts = []
        
#    i = 0
#    for val in sums: 
#        if val == 0: 
#                counts.append(i) 
#        i = i + 1

#    for array in listofBoth[1]: np.delete(array, counts)
        
#    current_list = listofBoth[1]
#    listofBoth[1] = np.unique(current_list, axis = 1) 
        
    tensor_features = []
    bitmaps = []
        
    for feature in listofBoth[0]: tensor_features.append(feature)
    
    for bitmap in listofBoth[1]: bitmaps.append(bitmap)
        
    tensor_features = np.array(tensor_features)
    bitmaps = np.array(bitmaps)

    X_train, X_test, y_train, y_test = train_test_split(tensor_features, bitmaps, test_size = 0.2)

    model = Sequential()
    model.add(Dense(12, input_dim = len(X_train[0]),  activation = 'relu'))
    model.add(Dense(24, activation = 'relu'))
    model.add(Dense(len(bitmaps[0]), activation = 'sigmoid'))

    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics=['accuracy'])
    model.fit(tensor_features, bitmaps, epochs = 150, batch_size = 100)
    analyzer = innvestigate.create_analyzer("gradient", model)
    userDepth = 10; 
    count = 0

    completeArr = []
    completeArr.append([tensor_features.tolist(), bitmaps.tolist()])
    for x in range(userDepth):
        
        gradientOutput = analyzer.analyze(tensor_features)
        new_features = tensor_features + gradientOutput 
        tensor_features = new_features
            
        newEdges = model.predict(tensor_features)
            
        i = 0
        jsonDict = {}
                
        for array in newEdges:
            jsonDict[dictID] = [np.round(new_features[i]).astype(int).tolist(), np.round(newEdges[i]).astype(int).tolist()]
            dictID = dictID + 1
            i = i + 1

        dictID = 0

    
    app_json = json.dumps(jsonDict)
    with open(os.path.join(str(folderID), str(iterID) + '_tendydemei.json'), 'w') as outfile:
            json.dump(json.loads(app_json), outfile)

    iterID += 1

 