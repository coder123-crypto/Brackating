#!/usr/bin/python

import sys
import getopt
import os
import subprocess

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "d:c:o:", ["delta=", "count=", "out-type="])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(1)

count = 3
delta = 0.33
outType = 'tiff'
for o, a in opts:
    if o in ('-d', '--delta'):
        delta = float(a)
    elif o in ('-c', '--count'):
        count = int(a)
    elif o in ('-o', '--out-type'):
        outType = a
    else:
        assert False, 'unhandled option'

AvailableTypes = ('ppm', 'tiff', 'tif', 'png', 'jpeg', 'jpg', 'fits')
if not outType in AvailableTypes:
    print('-o, --out-type can be only {0}'.format(AvailableTypes))
    exit(0)

AvailableExposures = {1:(0.0,), 
                      2:(-delta, delta), 
                      3:(-delta, 0.0, delta), 
                      5:(-2 * delta, -delta, 0.0, delta, 2 * delta), 
                      7:(-3 * delta, -2 * delta, -delta, 0.0, delta, 2 * delta, 3 * delta)}

outExposure = {}
if count in AvailableExposures.keys():
    for e in AvailableExposures[count]:
        outExposure[1.0 + e] = str(e) if e =< 0 else '+{0}'.format(e)
else:
    print('-c, --count can be only {0}'.format(AvailableExposures.keys()))
    exit(0)

processes = []     
for curFile in args:
    outDir = os.path.splitext(curFile)[0]
    if not os.path.exists(outDir):
        os.mkdir(outDir)
                
    for exp, fileName in outExposure.items():
        cmd = r'ufraw-batch --silent --overwrite --exposure={0} --out-type={1} {2} --output={3}/{4}.{1}'.format(exp, outType, curFile, outDir, fileName)
        processes.append(subprocess.Popen(cmd, shell = True))
            
for p in processes:
    p.wait()
