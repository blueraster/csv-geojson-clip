import os
import subprocess
import shutil
# GET Chris shape files
root = './'
shapeDir = os.path.join(root,'shp')
shpList = os.listdir(shapeDir)
dataFile = os.path.join(root,'data','lossyear-treecover-10-5000m.csv')
size = '5000'


def createGeoJSON():
    for i in shpList:
        fileName = i
        shapeFile = root+fileName+"/shp/"+fileName+".shp"
        outGeoJson = root+fileName+"/"+fileName+".geojson"
        proc = subprocess.Popen(['./shp2geojson.sh',outGeoJson,shapeFile])
        proc.wait()
        print fileName



def moveShapeFiles():
    for file in shpList:
        if file != 'main.py' and file != 'shp2geojson.sh' and file != '.DS_Store':
            countryISOName = root+file.split('.')[0]+"/"
            if not os.path.exists(countryISOName):
                os.makedirs(countryISOName+"shp")
            inputFile = root+file
            outputFile = countryISOName+"shp/"+file
            os.rename(inputFile, outputFile)

def makeoutputpath(path):
    if not os.path.exists(path):
        os.mkdir(path)
        #shutil.rmtree(path)
    return path


def temp():
    dataFile = '/Users/jnordling/projects/shape-temp/data/world-5000-bubble-2014.csv'
    geoJsonFile = '/Users/jnordling/projects/shape-temp/shp/NLD/NLD.geojson'
    iso = 'NLD'
    output = '/Users/jnordling/projects/shape-temp/shp/NLD/5000/COD-5000-bubble.csv'
    proc = subprocess.Popen(['./clip.sh', dataFile, geoJsonFile, iso, output])
    proc.wait()
    print 'Done'


def main():
    for dir in shpList:
        path = os.path.join(shapeDir,dir)
        if os.path.isdir(path):
            geoJsonFile = os.path.join(path,dir+'.geojson')
            iso = dir
            output = makeoutputpath(os.path.join(path,size))
            output = output+'/' + iso +'.csv'
            print 'Processing', iso
            proc = subprocess.Popen(['./clip.sh', dataFile, geoJsonFile, iso, output])
            proc.wait()



if __name__ == '__main__':
    main()