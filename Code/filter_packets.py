#FilterPackets Method
#Read & Filter ICMP Files from Node*.txt and output to Filtered_Node*.txt
def filterpackets() :
	print("called filterpackets function")
	#Lists for Data
	linelist = []
	headerlist = []
	icmplist = []
	#Files Node1 - Node4 will be opened and filtered
	for i in range(4):
		value = i+1
		fname = "Node"+str(value)+".txt"
		f = open('../Captures/'+fname,'r')
		fw = open('../Captures/Filtered_'+fname,'w') 
		line = f.readline()
		#Read file line by line
		while line:
			#add recently read line to list
			linelist.append(line)
			#next line
			line = f.readline()
		f.close()
		#Find Headers
		headerdata = list(filter(lambda a: "No." in a, linelist))
		#Find ICMP
		icmpdata = list(filter(lambda a: "ICMP" in a, linelist))
		#Print Data
		for j in range(len(icmpdata)):
			#Set Values
			icmp = icmpdata[j]
			header = headerdata[j]
			if ("unreachable" in icmp):
				continue
			#Add to lists
			headerlist.append(headerdata[j])
			icmplist.append(icmpdata[j])
			#Print / Write Values to file
			fw.write(str(header))
			fw.write(str(icmp))
			for k in range(47):
				value2 = k + 1
				#Find instance of ICMP in the line list
				dat = linelist.index(icmp)
				#Read next few lines after
				dats = linelist[dat+value2]
				if(dats == header):
					break
				else:
					fw.write(dats)

#Main Method
def main():
	filterpackets()
if __name__ == "__main__":
    main()