from dateutil.parser import parse
import csv
import math
import sys
import re

def parse_date(string, fuzzy=False):
    try: 
        return parse(string, fuzzy=fuzzy)
    except ValueError:
        return None


def parse_company(desc):
	comps = {	"apple":"shopping", 
				"trader joe's":"groceries", 
				"walgreens":"health", 
				"pet food express":"pet", 
				"rite aid":"health", 
				"target":"shopping", 
				"mcdonald's":"restaurant", 
				"hotelscom":"travel",
				"deckers":"shopping", 
				"safeway":"groceries", 
				"wholefds":"groceries", 
				"starbucks":"restaurant", 
				"natural grocers":"groceries", 
				"serenity medspa":"beauty", 
				"nijiya":"groceries", 
				"forever 21":"shopping", 
				"costco":"groceries", 
				"peet's":"restaurant", 
				"petrocan":"car", 
				"cdn tire store":"shopping", 
				"tim hortons":"restaurant", 
				"shell":"car", 
				"7-eleven":"restaurant", 
				"adidas":"shopping",
			}

	for k in comps:
		if desc.find(k) != -1:
			return (k, comps[k])

	return ("NA","NA")

gCSV = []

def parseInputText(filename):
	global gCSV

	print(f"Working on {filename}")

	lines = open(filename).readlines()

	for aline in lines:
		aline = aline.lower()
		aline = aline.strip()

		if len(aline) <= 11:
			continue

		rdate = parse_date(aline[:10])
		if rdate != None:
			rdate = aline[:10]
			rest = aline[11:]

			amounts = re.findall("-?\$\d*.\d*", rest)
			if len(amounts)<2 and len(amounts)>0 and amounts[0].startswith("-")==False:
				print(f"ERROR, not enough amounts in : {aline}")
				continue

			ramount = amounts[-1].replace("$","")
			ramount = float(ramount)

			endidx = rest.rfind("%")
			if endidx == -1:
				endidx = rest.find("$")

			rdesc = rest[:endidx-1].strip()
			rcompany, rcat = parse_company(rdesc)

			if rcat == "NA":
				print(f"Missing Cat : {rdesc}")
			
			gCSV.append([rdate, rcompany.capitalize(), rdesc.capitalize(), ramount, rcat.capitalize()])


		# if rdate != None :
		# 	rdate = values[r][AppleDateDesc][:10]
		# 	rdesc = values[r][AppleDateDesc][11:].lower()
		# 	rcompany, rcat = parse_company(rdesc)
		# 	ramount = float(values[r][AppleAmount][1:])

		# 	gCSV.append([rdate, rcompany, rdesc, ramount, rcat])

if __name__ == "__main__":
	if len(sys.argv) <= 1: 
		print("AppleStatementsToCSV.py inputfile")
		print("  Cut and Paste from Adobe Acrobat Reader all transaction into a text file")
		sys.exit(-1)
	
	for i in range(1, len(sys.argv)):
		parseInputText(sys.argv[i])

	if len(gCSV) > 0:
		with open('AppleStatementsExport.csv', 'w') as fp:
			writer = csv.writer(fp)
			writer.writerow(["Date", "Business", "Description", "Amount", "Category"])
			writer.writerows(gCSV)
