#!/usr/bin/python2
#Used to generate a xchainkeys config file (~/.config/xchainkeys/xchainkeys.conf)
#Should correspond to the Grid Your using in grid-wm

#usage:
#<file> -h <#> place "f" "f"
#<file> -h <#> makechains <-c> "blah" <-m>

from subprocess import call, check_output
from re import findall
import sys
import argparse

tiles = [
	[ '1', '2', '3', '4', '5', '6', '7', '8', '9', '0' ],
	[ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p' ],
	[ 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';' ],
	[ 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/' ]
]

def repositionWindow(squareA, squareB, screen, args):

	gridDimensions = {
		'width' : len(tiles[0]),
		'height' : len(tiles)
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
	call(['xdotool','getactivewindow','windowmove','--sync',str(startX),str(args.decheight+startY)])
	call(['xdotool','getactivewindow','windowsize','--sync',str(newWidth),str(newHeight-(args.decheight*2))])

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
	screensoutput=check_output(['xrandr','--current'])
	for screenNumber,screen in enumerate(findall('(.+) connected (\d+)x(\d+)+',screensoutput)):
		screens.append({
			'name' : screen[0],
			'width' : int(screen[1]),
			'height' : int(screen[2]),
			'offsetX' : 0
		})

	#Add offset if the window's x more than the first screen's width
	print screens
	if window['x'] > screens[0]['width']:
		screenNumber = 1
		screens[1]['offsetX'] = screens[0]['width']
	else:
		screenNumber = 0

	#Process ARGS to get pairs on the grid
	pairs = {}
	for index,arg in enumerate(args.keylist):
		for column,row in enumerate(tiles):
			for count, cell in enumerate(row):
				if cell == arg:
					label = 'start' if (index == 0) else 'end'
					pairs[label] =  { 'x' : count, 'y' : column }
	print pairs

	repositionWindow(pairs['start'], pairs['end'], screens[screenNumber], args)

def crawl(s,args):
	for row in tiles:
		for cell in row:
			replacements = {
				';' : "semicolon",
				',' : "comma",
				'.' : "period",
				'/' : "slash",
				}

			s1 = replacements.get(s, s)
			cell1 = replacements.get(cell, cell)
			print("{0.chain} {1} {2} :exec {3}"
			" -d {0.decheight} place '{4}' '{5}'".format(args,s1,cell1,\
														__file__,s,cell))

def makechains(args):
	if args.menu:
		print("feedback on")
		print("timeout 0")
		print("delay 0")
		print("foreground white")
		print("background black")

	#Continous Mode (doesnt stop resizing until hit Enter/Escape)
	if args.moded:
		print("{0.chain} :enter abort=manual".format(args))
		print("{0.chain} Return abort=manual".format(args))
		print("{0.chain} Escape abort=manual".format(args))

	#Generate all permutations (2 key presses)
	for row in tiles:
		for cell in row:
			crawl(cell,args)

parser = argparse.ArgumentParser(prog='generate-xchains', \
			description="Generates xchains for keyboard tiler")
subparsers = parser.add_subparsers(title='subcommands', \
			description='valid subcommands', \
			dest='subparser_name', \
			help='additional help')
chain_parser = subparsers.add_parser('makechains')
place_parser = subparsers.add_parser('place')

chain_parser.add_argument('-mn','--menu',help="Use dmenu?",action='store_true',default=False)
chain_parser.add_argument('-m','--moded', \
						help='Make it so it doesn\'t stop unless needed?', \
						action='store_true',default=False)
#Default Chain is Windows Keys (w) and x, Change this if wanted
chain_parser.add_argument('-c','--chain',help='Which keybinding starts the chain', default='W-x')
place_parser.add_argument('keylist', nargs=2)
parser.add_argument('-d','--decheight',help='Specified decoration height',type=int,default=20)
args = parser.parse_args(sys.argv[1:])

if args.subparser_name=='makechains':
	makechains(args)
elif args.subparser_name=='place':
	place(args)
else:
	print("Invalid command specified")
	exit(1)
