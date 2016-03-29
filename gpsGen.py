import random


#Buenos aires bounding box#
#NE -34.526562, -58.335159
#SW -34.705448, -58.531471

#Brussels bounding box#
#NE 50.913971, 4.43709
#SW 50.79628, 4.31393

#Baltimore bounding box#
#"NE 39.372082, -76.528961"
#"SW 39.197289, -76.711281"

#Paris bounding box#
#NE 48.902639, 2.410383
#SW 48.819812, 2.253411

#Berlin bounding box#
#NE 52.667511, 13.72616
#SW 52.330269, 13.05355

#Istanbul bounding box#
#NE 41.1528, 29.1838
#SW 40.97894, 28.60703

neLat = 41.1528
neLong = 29.1838

swLat = 40.97894
swLong = 28.60703

city = 'istanbul'

def generateNPoints(N, neLat, swLat, neLong, swLong):
    data = list()
    for i in range(0, N):
        lat = random.uniform(swLat, neLat)
        long = random.uniform(swLong, neLong)
        line = str(lat) + ", " +str(long)
        data.append(line)

    return data

def writeCSVFile(fileName, header, data):
    f = open(fileName, 'w')
    print >> f, header
    for row in data:
        print >> f, row
    f.close()



print "Hello mai"
for i in range(0, 10):
#i = 0
    gpsPoints = generateNPoints(100, neLat, swLat, neLong, swLong)
    writeCSVFile(city+"People" + str(i) +".csv", "lat, long", gpsPoints)
