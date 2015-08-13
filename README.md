# TSX-Trending-Value-Python-Script

-Program Overview-

The TSX Trending Value Python Script is based on the work of James O'Shaughnessy's book "What Works on Wall Street".
With some mofifications to O'Shaugnessy's Value Factor 2 Model, the program will return the top 25 ranked companies evaluated on
the Toronto Stock Exchange (TSX). The program fetches company data from the Yahoo Finance API and ranks its financials with respect 
to all other companies listed on the TSX. The top 25 caompanies are ranked and returned to the user in the Terminal.

- Installation & Operating Instructions- 

Note: This program is currently designed to be run using terminal/command line programs. Some knowledge of this software will be necessary.

For mac users:
  1. Place both the "Collect.py" and "TSX6.csv" files in the same directory.
  2. Open terminal on your computer, change directory to the directory where the files were placed.
  3. Run the "collect.py" file by typing "python collect.py" into the terminal shell.
  4. The terminal will run the program, results will be returned between 5-10 minutes
  
  - Sample Results - 
  
  Results will be returned in the following format:
  
  	______________________________________   

				Magellan Aero
				
				6 month change: 25.87
				
				PE:             15.46
				PE rank:        84.99
			
				PS:             0.00
				PS rank:        100.0
			 
				PB:             0.01
				PB rank:        100.0
				
				DY:             N/A
				DY rank:        50
				
				MC/EBITDA:      0.02
				MC/EBITDA rank: 100.0
			
				Company Rank:   434.99
			
				______________________________________   
  
  






