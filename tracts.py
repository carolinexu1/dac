import csv

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
    county = (row[1], row[2]) # the keys are tuples with (state, county)
    if county not in tracts.keys():
        tracts[county] = []
    if row[1] not in counties.keys(): # if state not in keys
        counties[row[1]] = set() # create set
    counties[row[1]].add(row[2]) # add the county to the list
    tracts[county].append(Tract(row[0], row[1], row[2], row[3]))
# theres 3220 counties

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
    sorting = []
    for r in result[0]: # for each tract in the county
        sorting.append((r, r.pop/totalPop - r.stops/busStops)) # the tract and the ratio diff
    sorting.sort(key=lambda x: x[1], reverse=True) # sort by who ahs the biggest diff
    for i in range(busStops - result[1]):
        sorting[i][0].stops += 1

busStops  = 54
county = ("Alabama", "Autauga County")
designate(county, busStops, tracts)
for tract in tracts[county]:
    print(tract.id, tract.stops)
