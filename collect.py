# Desktop/Software/python/StockAnalysis/TrendingValue
import csv
import urllib
import datetime
from decimal import Decimal

TSXtickers = []
# Data to be gathered for each company (Name, PE, P/S, P/B, dividend Yield, MC/EBITDA, % change)
UniverseListing = [[0 for i in range(13)] for i in range(43)]  # CHANGE TO 1793 companies total
#Ranking List ( PE rank, P/S rank, P/B rank, DY rank, MC/Ebitda rank)
DataRank = [[0 for i in range(5)] for i in range(43)]  #Change to 1793
StatPage = 'http://finance.yahoo.com/d/quotes.csv?s='


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

				
			if MCvalue and EBITDAvalue != 'N/A':
				
				UniverseListing[ArrayIndex][5] = Decimal(MCvalue) / Decimal(EBITDAvalue)
		
				if UniverseListing[ArrayIndex][5] < RatioMin and UniverseListing[ArrayIndex][5] > 0:
					RatioMin = UniverseListing[ArrayIndex][5]
			else:
				UniverseListing[ArrayIndex][5] = 'N/A'
				
		ArrayIndex += 1
	
	print  ' %s \t %s \t %s \t %s \t %s' % (PEmin,PSmin,PBmin,DYmax,RatioMin)
	return PEmin,PSmin,PBmin,DYmax,RatioMin

def SixMonthChange():

	ArrayIndex = 0
	
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
				
		UniverseListing[ArrayIndex][6] = round(Decimal(((CurrentPrice - PreviousPrice)/PreviousPrice)*100),2)
		
		
		ArrayIndex += 1
	print UniverseListing		

def DataRanker(PEmin,PSmin,PBmin,DYmax,RatioMin):

	i = 0
		
	for Company in UniverseListing:
		#Initialize counter to determine what companies maximum rank potential may be
		count = 0 
		RankSum = 0
	
		#################################### Assign PE Rank ##############################
		if Company[1] != "N/A":
			if Company[1] != PEmin:
				UniverseListing[i][7] = round((Decimal(PEmin)/(Decimal(Company[1]))*100),2)
		
			else:
				UniverseListing[i][7] = 100
			count +=1 
		else:
			UniverseListing[i][7] = 0    # If PE == "N/A" earnings are negative, assign 0 rank
			count +=1 
	
		#################################### Assign P/S Rank #############################
		if Company[2] != "N/A":
			if Company[2] != PSmin:
				UniverseListing[i][8] = round((Decimal(PSmin)/(Decimal(Company[2]))*100),2)
				count +=1 
			else:
				Company[2] = 100
				count +=1 
		else:
			UniverseListing[i][8] = "N/A" 
			
		#################################### Assign P/B Rank #############################
		if Company[3] != "N/A":
			if Company[3] != PBmin:
				UniverseListing[i][9] = round((Decimal(PBmin)/(Decimal(Company[3]))*100),2)
				count +=1 
			else:
				UniverseListing[i][9] = 100
				count +=1 
		else:
			UniverseListing[i][9] = "N/A" # If p/b == "N/A" ratio is not reported, therefore dont rank at all
			
		#################################### Assign Dividend Yield Rank ##################
		
		if Company[4] != "N/A":
			if Company[4] != DYmax:
				UniverseListing[i][10] = round(((Decimal(DYmax)-Decimal(Company[4]))/Decimal(DYmax)*100),2)
				count +=1 
			else:
				UniverseListing[i][10] = 100
				count +=1 
		else:
			UniverseListing[i][10] = "N/A" # If DY == "N/A", company does not pay dividends, do not rank
		
		
		###################################### Assign MC/EBITDA Rank  ###################
		if Company[5] != "N/A":
			if Company[5] != RatioMin or Company[5] == 0:
				UniverseListing[i][11] = round((Decimal(RatioMin)/((Company[5]))*100),2)
				count +=1 
			else:
				UniverseListing[i][11] = 100
				count +=1 
		else:
			UniverseListing[i][11] = "N/A" # If ratio == "N/A" ratio is not reported, therefore dont rank at all
		
		for j in range(7,12):
			if UniverseListing[i][j] != 'N/A':
				RankSum += Decimal(UniverseListing[i][j])
		CompanyRank = round(((RankSum / (count*100))*100),2)
		print ' %s / %s * 100   = %s' % (RankSum, count, CompanyRank)
		UniverseListing[i][12] = CompanyRank
			
		i += 1
	
		
		
(PEmin,PSmin,PBmin,DYmax,RatioMin) = DataCollector()
SixMonthChange()
DataRanker(PEmin,PSmin,PBmin,DYmax,RatioMin)

for company in UniverseListing:
			print company