#!/usr/bin/python
import csv,os,sys,re
verbose=0

# read text from csv input file and write out an EAGLE CAD drawing script

#inputfile = "ataridragon.txt"
#pixelwidth = 20.0
#layer = 201

#inputfile = "spaceinvader"
#pixelwidth = 20.0
#layer = 203

inputfile = "pitfallharry"
pixelwidth = 20.0
layer = 204

p = pixelwidth
pix = [0.0,0.0,0.0,0.0]
header = "# Jesse Hamner, 2016 \n\
GRID MIL 1 ON; \n\
CHANGE LAYER "

def printRect(tc, outfile):
    outfile.write("RECT (%0.3f %0.3f)(%0.3f %0.3f);\n" % 
        (tc[0],tc[1],tc[2],tc[3]))
    return True

def getRectWidth(xval, row):
    width = 1
    rowlength = len(row)
    if (row[xval] == "1"):
        while (xval + 1 < rowlength):
            xval = xval + 1
            if (row[xval] == "1"):
                width = width+1
            else:
                return width

    return (width)

# Main:

outfile = open (str("draw%s.scr" % inputfile), 'w')
outfile.write("%s%d;\n" % (header, layer) )

with open (str("%s.txt" % inputfile), 'r') as infile:
    arr=csv.reader(infile)
    data = list(arr)
    if verbose:
        print(str(data))
    rows = len(data)
    if verbose:
        print("Records found: %d" % rows)

    height = rows * p # beware the off by one error potential here

    if verbose:
        print ("Array height: %0.2f" % height)
    for i in range(0,rows):
        col = list(data[i])
        if verbose:
            print("Row %d" % i)
            print(str(col))

        cols = len(col)
        width = 1
        j = 0
        while(j < cols):
            if data[i][j] == "1":
                pix[0] = (j * p)
                pix[1] = height - p
                pix[3] = height

                try:
                    width = getRectWidth(j, data[i])

                except:
                    width = 1

                pix[2] = (j + width) * p
                printRect(pix, outfile)
                j = j + width
                width = 1
            else:
                j = j + 1

        height = height - p

outfile.write("# EOF\n")
outfile.close()

