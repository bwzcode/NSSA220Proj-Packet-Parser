def parse() :
	print('called parse function in packet_parser.py')
	#list for line storage	
	linelist=[]
	#lists of lists of icmp data. number corresponds to node
	parsedData1=[] 
	parsedData2=[]
	parsedData3=[]
	parsedData4=[]
	for i in range(4):
		fname = "Filtered_Node"+str(i+1)+".txt"
		f = open('../Captures/'+fname,'r')
		line = f.readline()
		while line:
			linelist.append(line)
			line=f.readline()
		f.close()
		icmpdata = list(filter(lambda a: "ICMP" in a, linelist))
		for d in icmpdata:
			d.strip()
			subList=d.split(None,6)
			if i == 0:
				parsedData1.append(subList)
			elif i == 1:
				parsedData2.append(subList)
			elif i== 2:
				parsedData3.append(subList)
			else:
				parsedData4.append(subList)
	return parsedData1,parsedData2,parsedData3,parsedData4
parse()			
		
	
	
