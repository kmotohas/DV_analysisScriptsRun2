import sys
import types

if len(sys.argv) != 3:
    #print(sys.argv)
    print('Usage: python lumicalc.py <start run number> <end run number>')
    exit(0)

start = int(sys.argv[1])
end = int(sys.argv[2])

#version = 'data16_13TeV.periodAllYear_DetStatus-v83-pro20-15_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns'
version = 'data16_13TeV.periodAllYear_DetStatus-v83-pro20-15_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns_DAOD_RPVLL_r8669'
f = open('lumitable-' + version + '.csv', 'r')

sum_lumi = 0.
for line in f:
    items = line.split(',')
    #print(type(items[0]))
    #if not isinstance(items[0], int):
    #    continue
    try:
        run = int(items[0])
        lumi = float(items[6])
        if start <= run <= end:
            print(run, lumi)
            sum_lumi += lumi
    except (TypeError, ValueError):
        continue

print(sum_lumi)
