#!/bin/bash
# Program to convert image output from EagleCAD to a print-friendly format.
# Note this script requires ImageMagick to be installed.
# Jesse Hamner, July 2016

function trimnegate {
    echo "Converting $1.png to $2.png:"
    convert "$1.png" -trim -negate $3 "$2.png" 
    rm "$1.png"
}

# To create the full color image but keep the color information:
IMG="fullcolorboard"
DEST="colorlayout"
echo "Converting ${IMG}.png to ${DEST}.png:"
convert ${IMG}.png -transparent black  ${IMG}NB.png
convert ${IMG}NB.png -alpha off -trim -fuzz 10% -fill white -opaque black \
 ${DEST}.png

# To invert the colors of the multi-layer monochrome image:
IMG="boardlayout"
trimnegate "${IMG}" "white${IMG}"

# To invert the colors of the top/bottom layer and convert to grayscale:
DEST="toplayout"
IMG="board${DEST}"
trimnegate "${IMG}" "${DEST}" "-colorspace gray -gamma 0.3 " # improve contrast

DEST="bottomlayout"
IMG="board${DEST}"
trimnegate "${IMG}" "${DEST}" "-colorspace gray -flop -gamma 0.3 " # and reverse image

# Do the silkscreen layers :
DEST="topsilk"
IMG="board${DEST}"
trimnegate "${IMG}" "${DEST}"

DEST="bottomsilk"
IMG="board${DEST}"
trimnegate "${IMG}" "${DEST}" "-flop" # reverse the bottom image 

DEST="dimensions"
IMG="board${DEST}"
trimnegate "${IMG}" "${DEST}" "-colorspace gray -gamma 0.9 " # improve contrast

convert APCschematic.png -gamma 0.95 -brightness-contrast -20x60 APCschembetter.png

# Clean up:
for F in fullcolorboardNB fullcolorboard 
do
    if [ -e "${F}.png" ]; then
        rm ${F}.png
    fi
done
# <EOF>
