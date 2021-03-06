#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from math import *


def trace(function, xmin, xmax, nstep, output):
	functionText = function
	output.write("x, %s\n" % function)
	function = eval("lambda x:" + function)

	step = 1.*(xmax-xmin)/nstep
	for i in range(nstep+1):
		x = xmin + i*step
		try:
			y = function(x)
		except:
			sys.stderr.write("Cannot compute %s with x = %.2f\n" % (functionText, x))
			sys.exit(-1)

		output.write("%s, %s\n" % (x, y))


def tracePS(function, xmin, xmax, nstep, output):
	functionText = function
	function = eval("lambda x:" + function)

	stepX = 1.*(xmax-xmin)/nstep # Calcul de la largeur d'un pas (en X)
	nstep = nstep + 1 # On calcule un point de plus pour bien prendre la valeur xmax.
	ymin = None # Valeur minimum en y
	ymax = None # Valeur maximum en y

	# Récupération des valeurs de la fonction
	# Récupération du max et du min en Y
	y = [] # Liste des valeurs de la fonction
	for i in range(nstep):
		x = xmin + i * stepX

		try:
			# output.write("x=%f | y=%f\n" % (x,function(x)))
			y.append(function(x))
			if ymax is None or y[i] > ymax :
				ymax = y[i]
			if ymin is None or y[i] < ymin :
				ymin = y[i]
		except:
			sys.stderr.write("Cannot compute %s with x = %.2f\n" % (functionText, x))
			sys.exit(-1)

	grid_xSize = 1.5 # Taille en cm d'un carreau de la grille en X
	grid_ySize = 1.5 # Taille en cm d'un carreau de la grille en Y

	grid_xStep = 10 # Nombre de carreau dans la grille sur X
	grid_yStep = 10 # Nombre de carreau dans la grille sur Y

	ratioY = (grid_ySize * grid_yStep) / (ymax - ymin); # Calcul du ratio en X
	ratioX = (grid_xSize * grid_xStep) / (xmax - xmin); # Calcul du ratio en Y

	stepY = 1.*(ymax-ymin)/grid_yStep # Calcul de la largeur d'un pas (en Y)

	# Calcul de la position de l'origine (sur une feuille au format A4)
	xOrigin = (21.0 - (grid_xStep * grid_xSize)) / 2.0
	yOrigin = (29.7 - (grid_yStep * grid_ySize)) / 2.0

	# Function prep_file
	output.write("%!\n")
	output.write("/cm { 28.3464567 mul } def\n")
	# end function prep_file

	# Function build_repere
	output.write("/grid {\n")
	output.write("    /Arial findfont\n")
	output.write("    .35 cm scalefont\n")
	output.write("    setfont\n")
	output.write("    newpath\n")
	output.write("    [3 3] 0 setdash\n")
	output.write("    0.5 setlinewidth\n")
	reset = False
	for wI in range(0, grid_xStep+1):

		xValue = xmin+wI*stepX*(nstep/grid_xStep)
		if xValue == 0.:
			output.write("    stroke\n")
			output.write("    [ ] 0 setdash\n")
			output.write("    1 setlinewidth\n")
			reset = True
		# Graduation sur l'axe X
		output.write("    %f cm %f cm moveto\n" % (xOrigin + grid_xSize * wI - 0.5, yOrigin - 1))
		output.write("    (%.1f) show\n" % (xValue))
		output.write("    %f cm %f cm moveto\n" % (xOrigin + grid_xSize * wI, yOrigin))
		output.write("    %f cm %f cm lineto\n" % (xOrigin + grid_xSize * wI, yOrigin + grid_ySize * grid_yStep))
		if reset:
			reset = False
			output.write("    stroke\n")
			output.write("    0.5 setlinewidth\n")
			output.write("    [3 3] 0 setdash\n")

		yValue = ymin+wI*stepY
		if yValue == 0.:
			output.write("    stroke\n")
			output.write("    1 setlinewidth\n")
			output.write("    [ ] 0 setdash\n")
			reset = True
		# Graduation sur l'axe Y
		output.write("    %f cm %f cm moveto\n" % (xOrigin - 2 , yOrigin + grid_ySize * wI))
		output.write("    (%.1f) show\n" % (yValue))
		output.write("    %f cm %f cm moveto\n" % (xOrigin, yOrigin + grid_ySize * wI))
		output.write("    %f cm %f cm lineto\n" % (xOrigin + grid_xSize * grid_xStep, yOrigin + grid_ySize * wI))
		if reset:
			reset = False
			output.write("    stroke\n")
			output.write("    0.5 setlinewidth\n")
			output.write("    [3 3] 0 setdash\n")
	output.write("    stroke\n")

	output.write("    [ ] 0 setdash\n")
	output.write("    stroke\n")
	output.write("} def\n")
	# End function build_repere
	output.write("grid\n")
	output.write("%f cm %f cm moveto\n" % (xOrigin, yOrigin - 5))
	output.write("(%s) show\n" % (functionText))

	output.write("newpath\n")
	output.write("0.8 setlinewidth\n")

	# Déplace le point origine en Y (en cas de valeur de y négative)
	yOrigin = yOrigin - ymin * ratioY
	output.write("%f cm %f cm moveto\n" % (xOrigin, yOrigin + y[0]*ratioY))
	i = 0
	for value in y:
		# output.write("%f, %f -> " % (key, value));
		x = i*stepX
		output.write("%f cm %f cm lineto\n" % (xOrigin + x*ratioX , yOrigin + value*ratioY ))
		i += 1

	# Function end_file
	output.write("stroke\n")
	output.write("showpage\n")
	# end function end_file




def usage(aFileOut):
	aFileOut.write("usage: trace.py [options] \"<function-name>\"\n")
	aFileOut.write("\nAvailable options : \n")
	aFileOut.write("\t-h, --help :  print help\n")
	aFileOut.write("\t-o, --output :  in outputfile\n")
	aFileOut.write("\t--xmin  :  set the minimum value of x\n")
	aFileOut.write("\t--xmax  :  set the maximum value of x\n")
	aFileOut.write("\t--nstep :  set how many steps\n")
	aFileOut.write("\n\nThis sentence ... help you.\n")


def main(argv=None):
	if argv is None:
		argv = sys.argv

	import getopt
	try:
		options, argv = getopt.getopt(argv[1:], "o:h", ["output=", "help", "xmin=", "xmax=", "nstep="])
	except getopt.GetoptError as message:
		sys.stderr.write("%s\n" % message)
		raise
		assert False, "unhandled option"


	output = sys.stdout
	xmin, xmax = 0., 1.
	nstep = 10

	for option, value in options:
		if option in ["-o", "--output"]:
			output = file(value, "w")

		elif option in ["-h", "--help"]:
			raise Exception("")

		elif option == "--nstep":
			try:
				nstep=int(value)
				if nstep <= 0:
					raise ValueError
			except ValueError:
				sys.stderr.write("nstep value error. Integer greater than 0 expected.\n")
				sys.exit(-1)


		elif option == "--xmin":
			try:
				xmin=float(value)
			except ValueError:
				sys.stderr.write("xmin value error. Float expected.\n")
				sys.exit(-1)

		elif option == "--xmax":
			try:
				xmax=float(value)
			except ValueError:
				sys.stderr.write("xmax value error. Float expected.\n")
				sys.exit(-1)
		else:
			help(sys.stderr)
			assert False, "unhandled option"

	if len(argv) != 1:
		raise Exception("Cannot understand the function\n")
		sys.exit(1)

	function = argv[0]

	if(output != sys.stdout):
		tracePS(function, xmin, xmax, nstep, output)
	else:
		trace(function, xmin, xmax, nstep, output)


if __name__ == "__main__":
	try:
		sys.exit(main())
	except AssertionError:
		usage(sys.stderr)
		sys.exit(-1)
	except SyntaxError:
		sys.stderr.write("The function is incomplete or wrong.\n")
		sys.exit(-1)
	except Exception as err:
		sys.stderr.write("%s\n" % err)
		usage(sys.stderr)
		sys.exit(-1)
