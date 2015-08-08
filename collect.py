# Desktop/Software/python/StockAnalysis/TrendingValue
import csv
import heapq
import urllib
import datetime
from decimal import Decimal

TSXtickers = []
Months = [[0,31],[1,28],[2,31],[3,30],[4,31],[5,30],[6,31],[7,31],[8,30],[9,31],[10,30],[11,31]]
# Data to be gathered for each company (Name, PE, P/S, P/B, dividend Yield, MC/EBITDA, % change)
UniverseListing = [[0 for i in range(13)] for i in range(1486)]  # CHANGE TO 1793 companies total
StatPage = 'http://finance.yahoo.com/d/quotes.csv?s='


#Generate FULL TSX stock listing
TSXcsvfile = "TSX6.csv"
ListingObject = open(TSXcsvfile, 'rU')	
ListingReader = csv.DictReader(ListingObject)	

#Generate List of TSX stocks
a = 0
for row in ListingReader:
	TSXtickers.append(row['Symbol'])
	UniverseListing[a][0] = row['Description']
	a +=1

def DataCollector():
	
	ArrayIndex = 0
	
	PEmin = 10000
	PSmin = 10000
	PBmin = 10000
	DYmax = 0
	RatioMin = 10000

	for Ticker in TSXtickers:

		file = StatPage + Ticker + '&f=' + 'nrp5p6yj1j4'
		file_object = urllib.urlopen(file)
		reader = csv.reader(file_object)
		
		
		#Assign Data to List
		
		for row in reader:
		
			############Assign PE and determine Min value
			
			if row[1] != 'N/A':
				UniverseListing[ArrayIndex][1] = Decimal(row[1])
			else:
				UniverseListing[ArrayIndex][1] = row[1]
			if UniverseListing[ArrayIndex][1] < PEmin:
				PEmin = UniverseListing[ArrayIndex][1]
					
			############Assign PS and determine Min value
			if row[2] != 'N/A':
				UniverseListing[ArrayIndex][2] = Decimal(row[2])	
			else:
				UniverseListing[ArrayIndex][2] = row[2]
				
			if UniverseListing[ArrayIndex][2] < PSmin:
				PSmin = UniverseListing[ArrayIndex][2]
				
			#############Assign PB and determine Min value
			if row[3] != 'N/A':
				UniverseListing[ArrayIndex][3] = Decimal(row[3])	
			else:
				UniverseListing[ArrayIndex][3] = row[3]
				
			if UniverseListing[ArrayIndex][3] < PBmin:
				PBmin = UniverseListing[ArrayIndex][3] 
				
			##############Assign DY and determine max value
			if row[4] != 'N/A':
				UniverseListing[ArrayIndex][4] = Decimal(row[4])
				
				if UniverseListing[ArrayIndex][4] > DYmax:
					DYmax = UniverseListing[ArrayIndex][4]
			else:
				UniverseListing[ArrayIndex][4] = row[4]
				
			#############Determine MC/EBITDA and Min value
			MCvalue = row[5]
			
			if 'M' in row[5]:
			
				MCvalue = MCvalue.replace(MCvalue[-1:],'')
				MCvalue = Decimal(MCvalue)*1000000
				
			if 'B' in row[5]:
				MCvalue = MCvalue.replace(MCvalue[-1:],'')
				MCvalue = Decimal(MCvalue)*1000000000
				
			EBITDAvalue = row[6]
			
			if 'M' in row[6]:
			
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000
				
			if 'B' in row[6]:
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000000

				
			if MCvalue !='N/A' and EBITDAvalue != 'N/A':
				if EBITDAvalue != '0.00':
					UniverseListing[ArrayIndex][5] = Decimal(MCvalue) / Decimal(EBITDAvalue)
		
				if UniverseListing[ArrayIndex][5] < RatioMin and UniverseListing[ArrayIndex][5] > 0:
					RatioMin = UniverseListing[ArrayIndex][5]
			else:
				UniverseListing[ArrayIndex][5] = 'N/A'
				
		ArrayIndex += 1
	
	print  ' %s \t %s \t %s \t %s \t %s' % (PEmin,PSmin,PBmin,DYmax,RatioMin)
	return PEmin,PSmin,PBmin,DYmax,RatioMin
	print 'Completed'

def SixMonthChange():

	ArrayIndex = 0
	
	BasePage = 'http://real-chart.finance.yahoo.com/table.csv?s='
	
	#Determine Today's Date
	CurrentDate = str(datetime.date.today()).split('-')
	ReferenceDay = CurrentDate[2]


	#Determine 6 Month Previous Corresponding Month and Year
	if CurrentDate[1]  < 6:
			PreviousMonth = 12 + (int(CurrentDate[1]) - 6)
			PreviousYear = int(CurrentDate[0]) - 1
	else:
			PreviousYear = int(CurrentDate[0])
			PreviousMonth = int(CurrentDate[1]) - 6
	
	#Check to see if today is a weekday
	CurrentWeekDay = datetime.date.weekday(datetime.date.today())
	CurrentWeekDay = 5

	#If today is saturday, adjust to fridays date. If necessary adjust previous month
	if CurrentWeekDay == 5:
		if int(CurrentDate[2]) ==1:
			CurrentDate[2] = int(Months[int(CurrentDate[1])-2][1])
			CurrentDate[1] = int(Months[int(CurrentDate[1])-2][0])+1
			
		else:	
			CurrentDate[2] = int(CurrentDate[2])-1
			
	#If today is Sunday, adjust to fridays date. If necessary adjust previous month	
	if CurrentWeekDay ==6:
		if int(CurrentDate[2]) == 1:
			CurrentDate[2] = int(Months[int(CurrentDate[1])-2][1]) -1
			CurrentDate[1] = int(Months[int(CurrentDate[1])-2][0]) +1	
		elif int(CurrentDate[2]) == 2:
			CurrentDate[2] = int(Months[int(CurrentDate[1])-2][1])	
			CurrentDate[1] = int(Months[int(CurrentDate[1])-2][0]) +1
		else:
			CurrentDate[2] = int(CurrentDate[2])-2
	
	#Determine 6 Month previous Corresponding Day

	PreviousDay = int(ReferenceDay)
	PreviousMonthEnd = int(Months[PreviousMonth-1][1])
	
	if PreviousDay > PreviousMonthEnd:
		PreviousWeekDay = datetime.date.weekday(datetime.date(PreviousYear,PreviousMonth,PreviousMonthEnd))

		if PreviousWeekDay == 5:
			PreviousDay = PreviousMonthEnd -1
		if PreviousWeekDay == 6:
			PreviousDay = PreviousMonthEnd - 2
		else:
			PreviousDay = PreviousMonthEnd
		
		Previous_Date_string = str(datetime.date(PreviousYear,PreviousMonth,PreviousDay))
		print Previous_Date_String
		
	else:
		PreviousWeekDay = datetime.date.weekday(datetime.date(PreviousYear,PreviousMonth,PreviousDay))
		
		if PreviousWeekDay == 5:
			if PreviousDay ==1:
				PreviousDay = Months[PreviousMonth-2][1]
				PreviousMonth = Months[PreviousMonth-2][0]+1
			else:
				PreviousDay = PreviousDay - 1
	
		if PreviousWeekDay == 6:
			if PreviousDay ==1:
				PreviousDay = Months[PreviousMonth-2][1]-1
				PreviousMonth = Months[PreviousMonth-2][0]+1
			elif PreviousDay == 2:
		
				PreviousDay = Months[PreviousMonth-2][1]
				PreviousMonth = Months[PreviousMonth-2][0] + 1
			else:
				PreviousDay = PreviousDay - 2
			
		Previous_Date_string = str(datetime.date(PreviousYear,PreviousMonth,PreviousDay))
		
		for Ticker in TSXtickers:
				
			#Create URL to fetch price changes
			file = BasePage + Ticker +'&d='+str(int(CurrentDate[1])-1)+'&e='+str(CurrentDate[2])+'&f='+CurrentDate[0]+'&g=d&a='+str(PreviousMonth-1)+'&b='+ str(PreviousDay) + '&c=' + str(PreviousYear) + '&ignore=.csv'
			file_object = urllib.urlopen(file)
			pricereader = csv.DictReader(file_object)
			
			z = 0
				
			#Read CSV, take first line as current price, search for previous date string to find previous price
			for row in pricereader:
			
				z+=1 
				if z==1:
					try:
						CurrentPrice = Decimal(row['Close'])
					except KeyError:
						print Ticker
						
				else:
					try:
						if row['Date'] == Previous_Date_string:
							PreviousPrice = Decimal(row['Close'])
					except KeyError:
						print Ticker
	    	
			UniverseListing[ArrayIndex][6] = round(Decimal(((CurrentPrice - PreviousPrice)/PreviousPrice)*100),2)
			
			ArrayIndex += 1		
	print 'Completed'

def DataRanker(PEmin,PSmin,PBmin,DYmax,RatioMin):

	i = 0
		
	for Company in UniverseListing:
		#Initialize counter to determine what companies maximum rank potential may be
		count = 0 
		RankSum = 0
	
		#################################### Assign PE Rank ##############################
		if Company[1] != "N/A":
			if Company[1] != PEmin and Company[1] != 0:
				UniverseListing[i][7] = round((Decimal(PEmin)/(Decimal(Company[1]))*100),2)
			elif Company[1] ==0:
				UniverseListing[i][7] = 0
				count +=1
			else:
				UniverseListing[i][7] = 100
			count +=1 
		else:
			UniverseListing[i][7] = 0    # If PE == "N/A" earnings are negative, assign 0 rank
			count +=1 
	
		#################################### Assign P/S Rank #############################
		if Company[2] != "N/A":
			if Company[2] != PSmin and Company[2] !=0:
				UniverseListing[i][8] = round((Decimal(PSmin)/(Decimal(Company[2]))*100),2)
				count +=1 
			elif Company[2] ==0:
				UniverseListing[i][8] = 0
				count +=1
			else:
				Company[2] = 100
				count +=1 
		else:
			UniverseListing[i][8] = "N/A" 
			
		#################################### Assign P/B Rank #############################
		if Company[3] != "N/A":
			if Company[3] != PBmin and Company[3] !=0:
				UniverseListing[i][9] = round((Decimal(PBmin)/(Decimal(Company[3]))*100),2)
				count +=1 
			elif Company[3] ==0:
				UniverseListing[i][9] = 0
				count +=1
			else:
				UniverseListing[i][9] = 100
				count +=1 
		else:
			UniverseListing[i][9] = "N/A" # If p/b == "N/A" ratio is not reported, therefore dont rank at all
			
		#################################### Assign Dividend Yield Rank ##################
		
		if Company[4] != "N/A":
			if Company[4] != DYmax:
				UniverseListing[i][10] = round(((Decimal(Company[4]))/Decimal(DYmax)*100),2)
				count +=1 
			else:
				UniverseListing[i][10] = 100
				count +=1 
		elif Company[4] == "N/A":
			UniverseListing[i][10] = "N/A" # If DY == "N/A", company does not pay dividends, do not rank
		
		
		###################################### Assign MC/EBITDA Rank  ###################
		if Company[5] != "N/A":
			if Company[5] != RatioMin and Company[5] != 0:
				UniverseListing[i][11] = round((Decimal(RatioMin)/((Company[5]))*100),2)
				count +=1 
				
			elif Company[5] == 0:
				UniverseListing[i][11] =0
				count +=1
			else:
				UniverseListing[i][11] = 100
				count +=1 
		else:
			UniverseListing[i][11] = "N/A" # If ratio == "N/A" ratio is not reported, therefore dont rank at all
		
		for j in range(7,12):
			if UniverseListing[i][j] != 'N/A':
				RankSum += Decimal(UniverseListing[i][j])
		
		if count >= 3:
			CompanyRank = round(((RankSum / (count*100))*100),2)
			UniverseListing[i][12] = CompanyRank
		else:
			UniverseListing[i][12] = 0
			
		i += 1
	
	print 'Completed'

	
SixMonthChange()	
(PEmin,PSmin,PBmin,DYmax,RatioMin) = DataCollector()
DataRanker(PEmin,PSmin,PBmin,DYmax,RatioMin)


#Return Top 25 Stocks and Display their Key Ratios and Rank
Top25rank = sorted(UniverseListing,key = lambda l: l[12])[-25:]
Top25Ordered = sorted(Top25rank, key = lambda x: abs(x[6]))[-25:]

CompanyIndex = 0

for Company in Top25rank:

	print """
				%s
				
				6 month change: %s
				
				PE:             %s
				PE rank:        %s
			
				PS:             %s
				PS rank:        %s
			 
				PB:             %s
				PB rank:        %s
				
				DY:             %s
				DY rank:        %s
				
				MC/EBITDA:      %s
				MC/EBITDA rank: %s
			
				Company Rank:   %s
			
				______________________________________   """  %(Top25rank[CompanyIndex][0], Top25rank[CompanyIndex][6],Top25rank[CompanyIndex][1],Top25rank[CompanyIndex][7],Top25rank[CompanyIndex][2],Top25rank[CompanyIndex][8],Top25rank[CompanyIndex][3],Top25rank[CompanyIndex][9],Top25rank[CompanyIndex][4],Top25rank[CompanyIndex][10], Top25rank[CompanyIndex][5],Top25rank[CompanyIndex][11],Top25rank[CompanyIndex][12])
				
	CompanyIndex += 1
			
