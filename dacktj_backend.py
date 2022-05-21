import json
import csv

def mainstuff(county, busStops):
    class Tract:
        def __init__(self, id, state, county, pop):
            self.id = id
            self.state = state
            self.county = county
            self.pop = int(pop)
            self.stops = 0
    
    file = open('acs2017_census_tract_data.csv')
    csvreader = csv.reader(file)
    header = next(csvreader) # the top row thats irrelevant
    tracts = dict()
    counties = dict() # keys r states and values are lists of counties
    for row in csvreader:
        c = (row[1], row[2]) # the keys are tuples with (state, county)
        if c not in tracts.keys():
            tracts[c] = []
        if row[1] not in counties.keys(): # if state not in keys
            counties[row[1]] = set() # create set
        counties[row[1]].add(row[2]) # add the county to the list
        tracts[c].append(Tract(row[0], row[1], row[2], row[3]))
    # theres 3220 counties
    print(tracts[county])
    
    def splitByTract(county, busStops, tracts, totalPop):
        usedStops = 0
        for t in tracts[county]:
            numStops = t.pop*busStops//totalPop # round down every time
            t.stops = numStops
            usedStops += numStops
        return (tracts[county], usedStops)
    
    def designate(county, busStops, tracts):
        totalPop = 0
        for t in tracts[county]:
            totalPop += t.pop # total population in a county
        result = splitByTract(county, busStops, tracts, totalPop)
        result[0].sort(key=lambda x: x.id)
        for tract in result[0]:
            print(tract.id, tract.stops)
        print()
        beforeExtra = dict()
        for t in result[0]:
            beforeExtra[t.id] = t.stops
        
        excess = busStops-result[1]
        sorting = []
        for r in result[0]: # for each tract in the county
            sorting.append((r, r.pop/totalPop - r.stops/busStops)) # the tract and the ratio diff
        sorting.sort(key=lambda x: x[1], reverse=True) # sort by who ahs the biggest diff
        for i in range(busStops - result[1]):
            sorting[i][0].stops += 1
        sorting.sort(key=lambda x: x[0].id)
        afterExtra = dict()
        for t in result[0]:
            afterExtra[t.id] = t.stops
        return (beforeExtra, excess, afterExtra)
    return designate(county, busStops, tracts)

def lambda_handler(event, context):
    param = event['rawQueryString']
    param = param.split("&")
    paramList = []
    for p in param:
        p = p.split("=")
        paramList.append(p[1])
    print(paramList[0]+" "+paramList[1].replace("%20", " ")+" "+paramList[2])
    result = mainstuff((paramList[0], paramList[1].replace("%20", " ")), int(paramList[2]))
    print(result)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
