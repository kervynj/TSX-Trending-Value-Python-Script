import csv
import urllib
import datetime
from decimal import Decimal

TSXtickers = []
# Data to be gathered for each company (Name, PE, P/S, P/B, dividend Yield, MC/EBITDA, % change)
UniverseListing = [[0 for i in range(7)] for i in range(43)]  # CHANGE TO 1793 companies total
#Ranking List ( PE rank, P/S rank, P/B rank, DY rank, MC/Ebitda rank)
DataRank = [[0 for i in range(5)] for i in range(43)]  #Change to 1793
StatPage = 'http://finance.yahoo.com/d/quotes.csv?s='
# Name, PE, P/S, P/B, dividend Yield, MC, EBITDA
StatsTag = ['n','r','p5','p6','y','j1','j4']


#Generate FULL TSX stock listing
TSXcsvfile = "TSXshort.csv"
ListingObject = open(TSXcsvfile, 'rU')	
ListingReader = csv.DictReader(ListingObject)	

#Generate List of TSX stocks
a = 0
for row in ListingReader:
	TSXtickers.append(row['Symbol'])
	UniverseListing[a][0] = row['Description']
	a +=1

	
######################################################################################Define Functions to gather all necessary data 
def SixMonthChange():

	c = 0
	
	BasePage = 'http://real-chart.finance.yahoo.com/table.csv?s='
	
	#Determine Today's Date
	CurrentDate = str(datetime.date.today()).split('-')
	
	#Check to see if today is a weekday
	CurrentWeekDay = datetime.date.weekday(datetime.date.today())
	#If today is saturday, adjust to fridays date
	
	if CurrentWeekDay == 5:
		CurrentDate[2] = int(CurrentDate[2]) - 1
	#If today is sunday, adjust to fridays date
	elif CurrentWeekDay ==6:
		CurrentDate[2] =  int(CurrentDate[2]) - 2
	
	#Determine 6 month previous date
	PreviousDay = int(CurrentDate[2])
	
	if CurrentDate[1]  < 6:
		PreviousMonth = 12 + (int(CurrentDate[1]) - 6)
		PreviousYear = int(CurrentDate[0]) - 1
	else:
		PreviousYear = int(CurrentDate[0])
		PreviousMonth = int(CurrentDate[1]) - 5
	
	#Check if previous date is a weekend, adjust accordingly	
	PreviousWeekDay = datetime.date.weekday(datetime.date(PreviousYear,PreviousMonth,int(CurrentDate[2])))
	
	if PreviousWeekDay == 5:
		PreviousDay = int(CurrentDate[2])-1
	elif PreviousWeekDay ==6:
		PreviousDay =  int(CurrentDate[2]) - 2
		
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
				CurrentPrice = Decimal(row['Close'])
		
			elif row['Date'] == Previous_Date_string:
				PreviousPrice = Decimal(row['Close'])
				
		UniverseListing[c][6] = round(Decimal(((CurrentPrice - PreviousPrice)/PreviousPrice)*100),2)
		
		c += 1		
	
def PEentry():

	j = 0
	PEmin = 10000

	for Ticker in TSXtickers:
		
		StatPeURL = StatPage + Ticker + '&f=' + StatsTag[1]
		StatPeObject = urllib.urlopen(StatPeURL)
		StatPeReader = csv.reader(StatPeObject)
		
		for row in StatPeReader:
		
			if row[0] != 'N/A':
				UniverseListing[j][1] = Decimal(row[0])
			
			else:
				UniverseListing[j][1] = row[0]
			
			if UniverseListing[j][1] < PEmin:
				PEmin = UniverseListing[j][1]
				
			j += 1
			
	print "done"
	print PEmin
	
	return PEmin
		
def PSentry():

	k = 0
	PSmin = 10000
	
	for Ticker in TSXtickers:
		
		StatPsURL = StatPage + Ticker + '&f=' + StatsTag[2]
		StatPsObject = urllib.urlopen(StatPsURL)
		StatPsReader = csv.reader(StatPsObject)
		
		for row in StatPsReader:
			 
			if row[0] != 'N/A':
				UniverseListing[k][2] = Decimal(row[0])
				
			else:
				UniverseListing[k][2] = row[0]
				
			if UniverseListing[k][2] < PSmin:
				PSmin = UniverseListing[k][2]
				
			k += 1
			
	print "done"
	return PSmin	
				
def PBentry():
	l = 0
	PBmin = 10000
	for Ticker in TSXtickers:
		
		StatPbURL = StatPage + Ticker + '&f=' + StatsTag[3]
		StatPbObject = urllib.urlopen(StatPbURL)
		StatPbReader = csv.reader(StatPbObject)
		
		for row in StatPbReader:
			if row[0] != 'N/A':
				UniverseListing[l][3] = Decimal(row[0])	
			else:
				UniverseListing[l][3] = row[0]
				
			if UniverseListing[l][3] < PBmin:
				PBmin = UniverseListing[l][3] 
				
			l += 1
			
	print "done"
	return PBmin
		
def DYentry():
	
	m = 0
	DYmax = 0
	for Ticker in TSXtickers:
		
		StatDyURL = StatPage + Ticker + '&f=' + StatsTag[4]
		StatDyObject = urllib.urlopen(StatDyURL)
		StatDyReader = csv.reader(StatDyObject)
		
		for row in StatDyReader:
			if row[0] != 'N/A':
				UniverseListing[m][4] = Decimal(row[0])
				
				if UniverseListing[m][4] > DYmax:
					DYmax = UniverseListing[m][4]
			else:
				UniverseListing[m][4] = row[0]
			
			m += 1
			
	print "done"
	return DYmax

def Ratioentry():
	
	n = 0
	
	RatioMin = 10000

	for Ticker in TSXtickers:
		
		StatMcURL = StatPage + Ticker + '&f=' + StatsTag[5]
		StatMcObject = urllib.urlopen(StatMcURL)
		StatMcReader = csv.reader(StatMcObject)
		
		for row in StatMcReader:
			MCvalue = row[0]
			
			if 'M' in row[0]:
			
				MCvalue = MCvalue.replace(MCvalue[-1:],'')
				MCvalue = Decimal(MCvalue)*1000000
				
			if 'B' in row[0]:
				MCvalue = MCvalue.replace(MCvalue[-1:],'')
				MCvalue = Decimal(MCvalue)*1000000000
				
		StatEbitdaURL = StatPage + Ticker + '&f=' + StatsTag[6]
		StatEbitdaObject = urllib.urlopen(StatEbitdaURL)
		StatEbitdaReader = csv.reader(StatEbitdaObject)
		
		for row in StatEbitdaReader:
			EBITDAvalue = row[0]
			
			if 'M' in row[0]:
			
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000
				
			if 'B' in row[0]:
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000000

				
		if MCvalue and EBITDAvalue != 'N/A':
		
			UniverseListing[n][5] = Decimal(MCvalue) / Decimal(EBITDAvalue)
			
			if UniverseListing[n][5] < RatioMin:
				RatioMin = UniverseListing[n][5]
		else:
			UniverseListing[n][5] = 'N/A'
			
			n += 1
			
	print "done"
	return RatioMin

def EBITDAentry():

	p = 0
	
	for Ticker in TSXtickers:
		
		StatEbitdaURL = StatPage + Ticker + '&f=' + StatsTag[6]
		StatEbitdaObject = urllib.urlopen(StatEbitdaURL)
		StatEbitdaReader = csv.reader(StatEbitdaObject)
		
		for row in StatEbitdaReader:
			EBITDAvalue = row[0]
			
			if 'M' in row[0]:
			
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000
				UniverseListing[p][6] = EBITDAvalue
				
			if 'B' in row[0]:
				EBITDAvalue = EBITDAvalue.replace(EBITDAvalue[-1:],'')
				EBITDAvalue = Decimal(EBITDAvalue)*1000000000
				UniverseListing[p][6] = EBITDAvalue
				
				
			
				
			p += 1
			
	print "done"
	
def RatioEntry():

	RatioMin = 10000
	
	for b in range(0,43):
	
		if UniverseListing[b][5] and UniverseListing[b][6] > 0:
		
			UniverseListing[b][7] = UniverseListing[b][5] / UniverseListing[b][6]
			
			if UniverseListing[b][7] < RatioMin:
				RatioMin = UniverseListing[b][7]
			
		else:
			UniverseListing[b][7] = 'N/A'
			
	return RatioMin
	print 'Done'
	
#Gather all data for TSX company listing			
SixMonthChange()
PEmin = PEentry()
PSmin = PSentry()
PBmin = PBentry()
DYmax = DYentry()
#MCentry()
#EBITDAentry()
RatioMin = Ratioentry()

print UniverseListing

#################################################################################################Trending Value Analysis

for x in range(0,43):  #change to 1793
	#Initialize counter to determine what companies maximum rank potential may be
	count = 0 
	RankSum = 0

	#Assign PE Rank
	if UniverseListing[x][1] != "N/A":
		if UniverseListing[x][1] != PEmin:
			DataRank[x][0] = Decimal(PEmin)/(Decimal(UniverseListing[x][1]))*100
			
		else:
			DataRank[x][0] = 100
		count +=1 
	else:
		DataRank[x][0] = 0    # If PE == "N/A" earnings are negative, assign 0 rank
		count +=1 
	
	#Assign P/S Rank
	if UniverseListing[x][2] != "N/A":
		if UniverseListing[x][2] != PSmin:
			DataRank[x][1] = Decimal(PSmin)/(Decimal(UniverseListing[x][2]))*100
			count +=1 
		else:
			DataRank[x][1] = 100
			count +=1 
	else:
		DataRank[x][1] = "N/A" # If p/s == "N/A" ratio is not reported, therefore dont rank at all
	
	#Assign P/B Rank
	if UniverseListing[x][3] != "N/A":
		if UniverseListing[x][3] != PBmin:
			DataRank[x][2] = Decimal(PBmin)/(Decimal(UniverseListing[x][3]))*100
			count +=1 
		else:
			DataRank[x][2] = 100
			count +=1 
	else:
		DataRank[x][2] = "N/A" # If p/b == "N/A" ratio is not reported, therefore dont rank at all
	
	#Assign Dividend Yield Rank
	if UniverseListing[x][4] != "N/A":
		if UniverseListing[x][4] != DYmax:
			DataRank[x][3] = (Decimal(DYmax)-Decimal(UniverseListing[x][4]))/Decimal(DYmax)*100
			count +=1 
		else:
			DataRank[x][3] = 100
			count +=1 
	else:
		DataRank[x][3] = "N/A" # If DY == "N/A", company does not pay dividends, do not rank
		
	#Assign MC/EBITDA Rank
	if UniverseListing[x][5] != "N/A":
		if UniverseListing[x][5] != RatioMin or 0:
			DataRank[x][4] = Decimal(RatioMin)/((UniverseListing[x][5]))*100
			count +=1 
		else:
			DataRank[x][4] = 100
			count +=1 
	else:
		DataRank[x][4] = "N/A" # If ratio == "N/A" ratio is not reported, therefore dont rank at all
		
	for i in range(1,5):
		if DataRank[x][i] != 'N/A':
			RankSum += Decimal(DataRank[x][i])
	CompanyRank = RankSum / (count*100)
	
	
	
	
		
	print """ %s
				
				PErank:                %s 
				PSrank:                %s
				PBrank:                %s
				DYrank:                %s
				MC/EBITDArank:		   %s
				Change:			   	   %s
				
				RANK:              %s 
				
				
			                              """ % (UniverseListing[x][0],DataRank[x][0],DataRank[x][1],DataRank[x][2],DataRank[x][3],DataRank[x][4],UniverseListing[x][6],CompanyRank)

					 
				


		
		
		


