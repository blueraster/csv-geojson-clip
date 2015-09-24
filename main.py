import os
import subprocess
# GET Chris shape files
root = '/Users/jnordling/projects/shape-temp/shp/'
## aws s3 sync s3://emerging-hotspots/Country_Geometry/CountriesPlateCarree_shp /Users/jnordling/projects/shape-temp/shp/
shpList = os.listdir(root)


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

def main():
    dataFile = '/Users/jnordling/projects/shape-temp/data/world-5000-bubble-2014.csv'
    geoJsonFile = '/Users/jnordling/projects/shape-temp/shp/NLD/NLD.geojson'
    iso = 'NLD'
    output = '/Users/jnordling/projects/shape-temp/shp/NLD/5000/COD-5000-bubble.csv'
    proc = subprocess.Popen(['./clip.sh',dataFile,geoJsonFile,iso,output])
    proc.wait()
    print 'Done'

if __name__ == '__main__':
    main()