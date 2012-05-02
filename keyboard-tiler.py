#!/usr/bin/python2
# keyboard-tiler: A CLI to positions windows on the grid of your screen using xdotool
# Usage:
# keyboard-tiler a/  (This would place the window on the bottom half of your screen)

#The Tiles you want to use for positioning, default is center of US Keyboard
from subprocess import call, check_output
from re import findall
import sys
from os import environ

tiles = [
	[ '1', '2', '3', '4', '5', '6', '7', '8', '9', '0' ],
	[ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p' ],
	[ 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';' ],
	[ 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/' ]
]
#Height of your window decorations, just set 0 if none

def repositionWindow(squareA, squareB, screen, args):

	gridDimensions = {
		'width' => len(tiles[0]),
		'height' => len(tiles)
	}

	#Make sure tiles go from left top most to bottom right most
	squareA = {
		'x' : sorted([squareA['x'], squareB['x']])[0],
		'y' : sorted([squareA['y'], squareB['y']])[0]
	}
	squareB = {
		'x' : sorted([squareA['x'], squareB['x']])[-1],
		'y' : sorted([squareA['y'], squareB['y']])[-1]
	}

	#Calculate Height and width factor based on passed screen and gridDimensions
	heightFactor = screen['height'] / gridDimensions['height']
	widthFactor  = screen['width']  / gridDimensions['width']

	#Calculate Start X and Y
	startX = screen['offsetX'] + (squareA['x'] * widthFactor)
	startY = squareA['y'] * heightFactor

	#Figure out how big to resize to
	newWidth = (squareB['x'] - squareA['x'] + 1) * widthFactor
	newHeight = (squareB['y'] - squareA['y'] + 1) * heightFactor

	#Fire to xdotool move and resize commands
	call(['xdotool','getactivewindow','windowmove','--sync',startX,args.height+startY])
	call(['xdotool','getactivewindow','windowsize','--sync',newWidth,newHeight-(args.height*2)])

def place(args):
	#Determine Current Window Values from xwin
	actwin = check_output(['xdotool', 'getactivewindow'])
	xwin = check_output(['xwininfo', '-id', actwin])
	window = {
		'x' : int(''.join(findall('Absolute upper-left X:\s+(\d+)',xwin)[0])),
		'y' : int(''.join(findall('Absolute upper-left Y:\s+(\d+)',xwin)[0])),
		'width' : int(''.join(findall('Width:\s+(\d+)',xwin)[0])),
		'height' : int(''.join(findall('Height:\s+(\d+)',xwin)))
	}

	#Get the Screens Dimensions from xrandr
	screens = []
	screensoutput=check_output('xrandr --current')
	for screenNumber,screen in enumerate(findall('(.+) connected (\d+)x(\d+)+',screensoutput)):
		screens[screenNumber] = {
			'name' : screen[0],
			'width' : int(screen[1]),
			'height' : int(screen[2]),
			'offsetX' : 0
		}

	#Add offset if the window's x more than the first screen's width
	if window['x'] > screens[0]['width']):
		screenNumber = 1
		screens[1]['offsetX'] = screens[0]['width']
	else:
		screenNumber = 0

	#Process ARGS to get pairs on the grid
	pairs = {}
	for arg,index in enumerate(findall('.',sys.argv[1]))
		for row, column in enumerate(tiles):
			for cell, count in enumerate(row):
				if cell == arg:
					label = (index == 0) ? 'start' : 'end'
					pairs[label] =  { 'x' : count, 'y' : column }

	repositionWindow(pairs['start'], pairs['end'], screens[screenNumber])
