import binascii
import emoji
import binascii
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

RED = '[color=ff0000]'
BLACK = '[color=ffffff]'
ORANGE_EMOJI = emoji.emojize(':tangerine:')

class ByteHolder():
	byteValue = ''
	byteColor = BLACK
	byteOffset = -1
	byteNextOffset = -1
	# This is a byte that was created as a filler when one file is longer than another
	byteFake = False
 
#-------------------

def get_hex_of(file):
	hexString = []
	isBlank = False
	x = 0
	with open(file, 'rb') as f:
		while(not isBlank):
			# Reads one byte at a time
			content = f.read(1)
			# Converts to hex then to useable string
			pw_bytes = binascii.hexlify(content)
			pw_bytes = pw_bytes.decode("utf-8")

			if(pw_bytes != ''):	
				bt = create_byte_object(pw_bytes.upper(), x, False)
				hexString.append(bt)
				x = x + 1
			else:
				isBlank = True
	return hexString

# takes a file in & then returns an array of arrays for the length of the file
def getHexOfInArray(file):
	hexString = []
	hexStringLine = []
	isBlank = False
	lineAmount = 0
	deleteThisCount = 0

	with open(file, 'rb') as f:
		while(not isBlank):
			#Read one byte at a time
			content = f.read(1)
			# Converts to hex then to useable string
			pw_bytes = binascii.hexlify(content)
			pw_bytes = pw_bytes.decode("utf-8")

			# Takes 16 bytes
			if(lineAmount != 16):
				# Add byte to an array
				hexStringLine.append(pw_bytes)
				lineAmount = lineAmount + 1
			else:
				# add array to final array
				hexString.append(hexStringLine)
				if (deleteThisCount == 0):
					print(hexStringLine)
					print(hexString[0])
					deleteThisCount = 1
				# Clear temp values
				hexStringLine.clear()
				lineAmount = 0
			# When the last byte is blank break out of while loop
			if(pw_bytes == ''):
				isBlank = True

	print(hexString[0])
	return hexString	

def getHexOfInDictionary(file):
	hexStringDict = {}
	isBlank = False
	byteCount = 0

	with open(file, 'rb') as f:
		while(not isBlank):
			# Read one byte at a time
			content = f.read(1)
			# Convert to hex then to useable string
			pw_bytes = binascii.hexlify(content)
			pw_bytes = pw_bytes.decode("utf-8")

			#hexStringDict.update({str(byteCount), pw_bytes})
			hexStringDict[str(byteCount)] = pw_bytes
			byteCount = byteCount + 1

			# When the lastdbye is blank, break out of while loop
			if(pw_bytes == ''):
				isBlank = True
	return getHexForScreen(hexStringDict)

# Separates the Dictionary of a file into an array
def getHexForScreen(fileDictionary):
	hexString = []
	hexStringLine = hex(0) + '\t\t'
	count = 0
	for i in range(len(fileDictionary)):
		if(count != 16):
			# Separates each section by 4 bytes with a space
			if(count == 4 or count ==8 or count ==12):
				hexStringLine = hexStringLine + ' '
			hexStringLine = hexStringLine + fileDictionary[str(i)]
			count = count + 1
		else:
			# makes sure the first offset is 0 instead of current i
			if(i > 20):
				hexStringLine = hex(i-1) + '\t\t' + hexStringLine
			# makes all upper case in order to keep similar size for characters
			hexStringLine = hexStringLine.upper()
			# Add current line to the array
			hexString.append(hexStringLine)
			# Reset parameters for next line
			hexStringLine = ''
			count = 0
	return hexString

def pick_file():
	print()
	Tk().withdraw()
	file = askopenfilename()
	return getHexOfInDictionary(file)


def pick_file_old():
	Tk().withdraw()
	file = askopenfilename()
	return get_hex_of(file)

def create_byte_object(value, offset, isFake):
	bt = ByteHolder()
	bt.byteValue = value
	bt.byteOffset = hex(offset)
	bt.byteNextOffset = hex(offset+1)
	bt.byteFake = isFake
	return bt

def save_to_string(data, file, i, ending):
	hexString = data + file[i].byteColor + file[i].byteValue + '[/color]' + ending
	return hexString



def spot_differences(file1,file2):
	files = []
	for i in range(len(file1)):
		if(file1[i].byteValue != file2[i].byteValue and not file1[i].byteFake and not file2[i].byteFake):
			file1[i].byteColor = RED
			file2[i].byteColor = RED
	files.append(file1)
	files.append(file2)
	return files


def format_files_in_hex(file1, file2):
	files = []
	# Adds blank characters at end of file to make both files same size
	if(len(file1) != len(file2)):
		if(len(file1) > len(file2)):
			sizeToAdd = len(file1) - len(file2)
			for x in range(sizeToAdd):
				bt = create_byte_object('  ', x, True)
				file2.append(bt)
		if(len(file1) < len(file2)):
			sizeToAdd = len(file2) - len(file1)
			for x in range(sizeToAdd):
				bt = create_byte_object('  ', x, True)
				file1.append(bt)

	# Shows the differences between the files
	filesWithDifferences = spot_differences(file1, file2)
	hexString1 = filesWithDifferences[0]
	hexString2 = filesWithDifferences[1]

	# Formats the strings for each file
	hexString1 = ''
	hexString2 = ''
	hexCount = ''
	for i in range (len(file1)):
		hexString1 = save_to_string(hexString1, file1, i, ' ')
		hexString2 = save_to_string(hexString2, file2, i, ' ')
		if((i+1)%4 == 0):
			hexString1 = hexString1 + '   '
			hexString2 = hexString2 + '   '
		if((i+1)%16 == 0):
			hexString1 = hexString1 + '\n'
			hexString2 = hexString2 + '\n'
			#if(i != len(file1)-1):
			hexCount = hexCount + str(file1[i].byteNextOffset) + '\n'

	# Returns files
	files.append(hexString1)
	files.append(hexString2)
	files.append(hexCount)
	return files