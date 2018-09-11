#last changed 9/11/2018 

#pdf merger will use list of pdfs to create merged file; filename for merged pdf is concatenated newsname (name of newspaper pulled from dictionary) and fn_1 (date) so can create this and add to line of metadata; 
#pdf merger file identification can be separate loop to avoid looping problem?

#to do -- 
#combining PDfs with new name
#write combined PDF to output folder

#done:
	#dictionary for looking up lccn and replacing with name of newspaper
	#creating PDF name from newspaper name and date of issue
	#fix loop problem; it is outputting blank lines and fields, and items with mismatched name and date 
	#need 2 dictionaries for title, one with name formatted for DC Title field (titlesf), one unformatted (titlesu) for pdf filename
	#write a line of CSV metadata for each issue in DC format
		#title (newspaper name & issue date), lccn, University of New Mexico, "Newspaper", publication date, language, #city_name, pdf filename (for matching with URL from Google Drive)
	#write metadata to CSV file in output folder for DC upload
	#create output folder for each newspaper on desktop

#importing libraries
import os
from os.path import join
import sys
import codecs
import cStringIO
import csv
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader

#functions
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
 
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

#metadata components for processing
lccn_1 = "" #library of congress catalog number for newspaper; used for looking up newspaper name in formatted and #unformatted dictionaries, and looking up city in coverage dictionary 
newsname = "" #unformatted newspaper title for pdf naming, desktop folder creation
fn_1 = "" #date formatted as year-mm-dd
fn_2 = "" #date formatted as mm-dd-year
pdfname = "" #concatenation of unformatted newspaper title and fn_1 date for naming merged PDF files

#digital commons metadata fields
titlef = "" #formatted newspaper title for DC metadata, eg "Mesilla Valley Independent, 03-12-1915"
city_name = "" #for DC coverage field
doctype = "newspaper" #document type for DC metadata
news_lang = "English" #change to Spanish manually in Excel for Spanish papers

#lists
pdfs = list()
dc_list = list()

#unformatted titles dictionary for file naming
titlesu = {"sn001" : "daily-planet", "sn002" : "daily-prophet", "sn565" : "amity-gazette", "sn5683a" : "antarctica-daily"}
#formatted titles dictionary for metadata entry
titlesf = {"sn001" : "The Daily Planet", "sn002" : "The Daily Prophet", "sn565" : "The Amity Gazette", "sn5683a" : "Antarctica Daily"}
coverage = {"sn001" : "Metropolis", "sn002" : "Diagon Alley", "sn565" : "Martha's Vineyard", "sn5683a" : "Antarctica"}

# this is going to be a loop problem -- need to loop through one date-named folder at a time and create that combined PDF, then go to the next date-named folder within the #lccn-named outer folder.

#walking through collection, filling variables and combining pdf files
for root, dirs, files in os.walk('.'): #starts in current directory
	
	#get folder name; put in variable - this is the lc serial number (lccn) for the newspaper
	
	dirname, fname = os.path.split(root)
	
	print "dirname is ", dirname
	print "fname is ", fname
	
	#getting LCCN
	if "sn" not in fname:
		pass
	else:
		lccn_1 = fname
		#print "serial # is ", lccn_1
	
	#getting folder names and parsing into date formats
	if not fname.startswith("1"):	
		pass
	else:
		fn_1 = fname[0:4] + "-" + fname[4:6] +  "-" + fname [6:8] #this is YYYY-MM-DD format for DC batch upload
		#print "fn_1 is ", fn_1
		
		fn_2 = fname[4:6] +  "-" + fname [6:8] + "-" + fname[0:4] #this is MM-DD-YYYY format for the item title in DC
		#print "fn_2 is ", fn_2
		
		#store fname as name of subdirectory to run pdf merger on files within it?
		#pdf merge loop here?
		
		
	#filling variables for metadata fields 
	if lccn_1 in titlesu:
		newsname = titlesu.get(lccn_1) + "-" + str(fn_1)
	#else:
		#newsname = "Unknown" + "-" + str(fn_1)
	
	#getting DC formatted item title
	if lccn_1 in titlesf:
		titlef = str(titlesf.get(lccn_1)) + ", " + str(fn_2)
	#else:
		#titlef = "Unknown" + "," + str(fn_2)
		
	#getting city_name
	if lccn_1 in coverage:
		city_name = coverage.get(lccn_1)
	#else:
		#city_name = "New Mexico"	
	
	#creating pathname for folder and file output
	#I don't think we need individual folders on desktop; might simplify script as long as output pdfs are named correctly?
	#same newspaper might be on multiple hard drives and output should go into one folder per newspaper
	out_path = "C:/Users/amywinter/Desktop/" + str(newsname)
	#print "output path is ", out_path
	
	#not doing this for now, to help simplify script
	#creating directory named for newspaper, to hold combined pdfs
	#if os.path.isdir(out_path): 
		#pass #skipping if desktop folder already exists for this newspaper
	#else:
		#os.mkdir(out_path)
			
	#adding values to lists
	#dc list:  title, lccn, "Newspaper", publication date, language, city_name, pdfname
	
	#if 'Unknown' not in titlef and fn_1 is not None:
	#dc_list.append(titlef)
	#dc_list.append(lccn_1)
	#dc_list.append(doctype)
	#dc_list.append(str(fn_1))
	#dc_list.append(news_lang)
	#dc_list.append(city_name)
	#dc_list.append(pdfname)
	
	#print dc_list
	
	# files are being opened in append mode so check output for duplicates
	#f = open("dc-metadata.csv", "ab")
	
	#wr = UnicodeWriter(f, delimiter="#", lineterminator='\r\n')
	#wr.writerow(dc_list)
	
	#f.close()

	#instructions for processing the metadata output in Excel, draft #1:  Highlight column D (publication date), press F5, #click "Special", click "Blanks", then on Home tab choose "delete sheet rows" - this gets rid of all repeats with #missing fields
	
	#concatenating the name of the newspaper plus the issue date for the name of the combined pdf file
	pdfname = "C:/Users/amywinter/Desktop/" +  newsname + ".pdf"
	print "pdfname is ", pdfname

	for filename in files:
		#print filename
	#if filename ends with .pdf, add to list; this will be the list of pdfs to merge with pdf merger
		if filename.endswith(".pdf"):
			#print filename
			pdfs.append(filename)
			print "pdf list is ", pdfs
			print "pdf list length is ", len(pdfs)
	
	if len(pdfs) > 0:
		print "Done adding PDFs for this folder!"
		
	#use the pdf combine script to combine the pdfs for that date, and name with date and newsname
	#PROBLEM:  This is printing PDF files that have 2 copies of the last file in the folder; first file is skipped #somehow
	merger = PdfFileMerger()

	for item in pdfs:
		input_path = os.path.join(dirname, fname, filename)
		input_path = os.path.normpath(input_path)
		merger.append(input_path, 'rb')
	
	with open(pdfname, 'wb') as fout:
		merger.write(fout)
				
	print "PDF PRINTED!!"
				
	#emptying out containers
	del pdfs[:]
	pdfname = ""
	#lccn_1 = ""
	newsname = ""
	fn_1 = ""
	fn_2 = ""
	del dc_list[:]
	
#titlesu = {"sn84020616" :"albuquerque-citizen", "sn84020613" :"albuquerque-daily-citizen", "sn84020615" :"albuquerque-evening-citizen", "sn92070581" :"albuquerque-evening-herald", "sn84031081" :"albuquerque-morning-journal", "sn92070464" :"albuquerque-weekly-citizen", "sn92070566" :"alamogordo-news", "sn92070564" :"alamogordo-news-advertiser", "sn92070450" :"belen-news", "sn87090373" :"black-range", "sn86083435" :"borderer", "sn93061429" :"carlsbad-current", "sn93061428" :"carlsbad-current", "sn93061430" :"carlsbad-current-nm-sun", "sn86063539" :"carrizozo-news", "sn94056939" :"carrizozo-outlook", "sn93061818" :"catron-county-news", "sn92070454" :"socorro-chieftain", "sn92070542" :"cimarron-citizen", "sn92070544" :"cimarron-news-citizen", "sn92070543" :"cimarron-news-press", "sn93061569" :"clayton-citizen", "sn94056928" :"clayton-enterprise", "sn93061573" :"clayton-news", "sn93061777" :"clovis-news", "sn92070539" :"columbus-courier", "sn92072379" :"cuervo-clipper", "sn86063579" :"deming-graphic", "sn83004264" :"deming-headlight", "sn93061403" :"dawson-news", "sn92070477" :"silver-city-eagle", "sn93061674" :"eddy-current", "sn87090070" :"capitan-farol", "sn92070404" :"belen-hispano-americano", "sn93061379" :"belen-hispano-americano", "sn94056852" :"las-vegas-el-independiente", "sn94056869" :"nuevo-mexicano", "sn93061466" :"estancia-news", "sn94057017" :"estancia-news-herald", "sn93061433" :"evening-current", "sn92070582" :"evening-herald", "sn94056832" :"fort-sumner-review", "sn86063589" :"gallup-herald", "sn92070445" :"lincoln-golden-era", "sn93061371" :"kenna-record", "sn83045030" :"bandera-americana", "sn83045398" :"revista-de-taos", "sn93061743" :"taos-revista-cresset", "sn94056834" :"taos-revista-news", "sn83045436" :"voz-del-pueblo", "sn93061467" :"nuevas-estancia", "sn90051703" :"las-vegas-daily-gazette", "sn86063592" :"las-vegas-daily-optic", "sn96061021" :"las-vegas-free-press", "sn84027457" :"las-vegas-gazette", "sn93061633" :"las-vegas-gazette", "sn93061631" :"las-vegas-morning-gazette", "sn92070417" :"las-vegas-optic", "sn92070422" :"las-vegas-stock-grower", "sn87090072" :"lincoln-county-leader", "sn91052379" :"cerrillos-rustler", "sn94005878" :"lovington-leader", "sn84027433" :"mesilla-times", "sn87090075" :"mesilla-valley-independent", "sn93061497" :"mesilla-weekly-times", "sn84020617" :"morning-journal", "sn92070567" :"morning-news", "sn93061704" :"mountainair-independent", "sn84024881" :"nm-review", "sn93061701" :"nm-state-record", "sn930617407" :"old-abe-eagle", "sn93061752" :"raton-comet", "sn91052387" :"raton-daily-independent", "sn91052388" :"raton-weekly-independent", "sn92070553" :"red-river-prospector", "sn93061795" :"reserve-advocate", "sn87090080" :"rio-grande-republican", "sn86063823" :"roswell-daily-record", "sn92072386" :"cerrillos-the-rustler", "sn93061544" :"san-jon-sentinel", "sn92070446" :"san-juan-county-index", "sn86063590" :"san-juan-times", "sn84020631" :"daily-new-mexican", "sn88071076" :"santa-fe-gazette", "sn88071075" :"santa-fe-weekly-gazette", "sn84022168" :"santa-fe-weekly-gazette", "sn84022165" :"santa-fe-weekly-gazette", "sn84020630" :"santa-fe-new-mexican", "sn84020626" :"santa-fe-new-mexican-review", "sn94057006" :"sierra-county-advocate", "sn92070455" :"socorro-chieftain", "sn86090503" :"socorro-chieftain", "sn86090456" :"southwest-sentinel", "sn92061524" :"spanish-american", "sn94057002" :"taiban-valley-news", "sn93061711" :"tucumcari-news-times", "sn93061709" :"tucumcari-news", "sn87067095" :"weekly-new-mexican-review", "sn87067094" :"weekly-new-mexican-review-livestock", "sn92070405" :"lordsburg-western-liberal", "sn87090065" :"white-oaks-eagle"}

#titlesf = {"sn84020616" : "Albuquerque Citizen", "sn84020613" : "Albuquerque Daily Citizen", "sn84020615" : "Albuquerque Evening Citizen", "sn92070581" : "Albuquerque Evening Herald", "sn84031081" : "Albuquerque Morning Journal", "sn92070464" : "Albuquerque Weekly Citizen", "sn92070566" : "Alamogordo News", "sn92070564" : "Alamogordo News-Advertiser", "sn92070450" : "Belen News", "sn87090373" : "Black Range", "sn86083435" : "Borderer", "sn93061429" : "Carlsbad Current", "sn93061428" : "Carlsbad Current", "sn93061430" : "Carlsbad Current and New Mexico Sun", "sn86063539" : "Carrizozo News", "sn94056939" : "Carrizozo Outlook", "sn93061818" : "Catron County News", "sn92070454" : "Chieftain", "sn92070542" : "Cimarron Citizen", "sn92070544" : "Cimarron News and Citizen", "sn92070543" : "Cimarron News and Press", "sn93061569" : "Clayton Citizen", "sn94056928" : "Clayton Enterprise", "sn93061573" : "Clayton News", "sn93061777" : "Clovis News", "sn92070539" : "Columbus Courier", "sn92072379" : "Cuervo Clipper", "sn86063579" : "Deming Graphic", "sn83004264" : "Deming Headlight", "sn93061403" : "Dawson News", "sn92070477" : "Eagle", "sn93061674" : "Eddy Current", "sn87090070" : "El Farol", "sn92070404" : "El Hispano Americano", "sn93061379" : "El Hispano-Americano", "sn94056852" : "El Independiente", "sn94056869" : "El Nuevo Mexicano", "sn93061466" : "Estancia News", "sn94057017" : "Estancia News-Herald", "sn93061433" : "Evening Current", "sn92070582" : "Evening Herald", "sn94056832" : "Fort Sumner Review", "sn86063589" : "Gallup Herald", "sn92070445" : "Golden Era", "sn93061371" : "Kenna Record", "sn83045030" : "La Bandera Americana", "sn83045398" : "La Revista de Taos", "sn93061743" : "La Revista de Taos and the Taos Cresset", "sn94056834" : "La Revista de Taos and the Taos Valley News", "sn83045436" : "La Voz del Pueblo", "sn93061467" : "Las Nuevas de la Estancia", "sn90051703" : "Las Vegas Daily Gazette", "sn86063592" : "Las Vegas Daily Optic", "sn96061021" : "Las Vegas Free Press", "sn84027457" : "Las Vegas Gazette", "sn93061633" : "The Las Vegas Gazette", "sn93061631" : "Las Vegas Morning Gazette", "sn92070417" : "Las Vegas Optic", "sn92070422" : "Las Vegas Weekly Optic and Stock Grower", "sn87090072" : "Lincoln County Leader", "sn91052379" : "Los Cerrillos Rustler", "sn94005878" : "Lovington Leader", "sn84027433" : "Mesilla Times", "sn87090075" : "Mesilla Valley Independent", "sn93061497" : "Mesilla Weekly Times", "sn84020617" : "Morning Journal", "sn92070567" : "Morning News", "sn93061704" : "Mountainair Independent", "sn84024881" : "New Mexican Review", "sn93061701" : "New Mexico State Record", "sn930617407" : "Old Abe Eagle", "sn93061752" : "Raton Comet", "sn91052387" : "Raton Daily Independent", "sn91052388" : "Raton Weekly Independent", "sn92070553" : "Red River Prospector", "sn93061795" : "Reserve Advocate", "sn87090080" : "Rio Grande Republican", "sn86063823" : "Roswell Daily Record", "sn92072386" : "Rustler", "sn93061544" : "San Jon Sentinel", "sn92070446" : "San Juan County Index", "sn86063590" : "San Juan Times", "sn84020631" : "Santa Fe Daily New Mexican", "sn88071076" : "Santa Fe Gazette", "sn88071075" : "Santa Fe Weekly Gazette", "sn84022168" : "Santa Fe Weekly Gazette", "sn84022165" : "Santa Fe Weekly Gazette", "sn84020630" : "Santa Fe New Mexican", "sn84020626" : "Santa Fe New Mexican and Review", "sn94057006" : "Sierra County Advocate", "sn92070455" : "Socorro Chieftain", "sn86090503" : "Socorro Chieftain", "sn86090456" : "Southwest-Sentinel", "sn92061524" : "Spanish American", "sn94057002" : "Taiban Valley News", "sn93061711" : "Tucumcari News and Tucumcari Times", "sn93061709" : "Tucumcari News", "sn87067095" : "Weekly New Mexican Review", "sn87067094" : "Weekly New Mexican Review and Live Stock Journal", "sn92070405" : "Western Liberal", "sn87090065" : "White Oaks Eagle"}

#coverage = {"sn84020616" : "Albuquerque, N.M.", "sn84020613" : "Albuquerque, N.M.", "sn84020615" : "Albuquerque, N.M.", "sn92070581" : "Albuquerque, N.M.", "sn84031081" : "Albuquerque, N.M.", "sn92070464" : "Albuquerque, N.M.", "sn92070566" : "Alamogordo, N.M.", "sn92070564" : "Alamogordo, N.M.", "sn92070450" : "Belen, N.M.", "sn87090373" : "Robinson, N.M.", "sn86083435" : "Las Cruces, N.M.", "sn93061429" : "Carlsbad, N.M.", "sn93061428" : "Carlsbad, N.M.", "sn93061430" : "Carlsbad, N.M.", "sn86063539" : "Carrizozo, N.M.", "sn94056939" : "Carrizozo, N.M.", "sn93061818" : "Reserve, N.M.", "sn92070454" : "Socorro, N.M.", "sn92070542" : "Cimarron, N.M.", "sn92070544" : "Cimarron, N.M.", "sn92070543" : "Cimarron, N.M.", "sn93061569" : "Clayton, N.M.", "sn94056928" : "Clayton, N.M.", "sn93061573" : "Clayton, N.M.", "sn93061777" : "Clovis, N.M.", "sn92070539" : "Columbus, N.M.", "sn92072379" : "Cuervo, N.M.", "sn86063579" : "Deming, N.M.", "sn83004264" : "Deming, N.M.", "sn93061403" : "Dawson, N.M.", "sn92070477" : "Silver City, N.M.", "sn93061674" : "Carlsbad, N.M.", "sn87090070" : "Capitan, N.M.", "sn92070404" : "Roy, N.M.", "sn93061379" : "Belen, N.M.", "sn94056852" : "Las Vegas, N.M.", "sn94056869" : "Santa Fe, N.M.", "sn93061466" : "Estancia, N.M.", "sn94057017" : "Estancia, N.M.", "sn93061433" : "Carlsbad, N.M.", "sn92070582" : "Albuquerque, N.M.", "sn94056832" : "Las Vegas, N.M.", "sn86063589" : "Gallup, N.M.", "sn92070445" : "Lincoln, N.M.", "sn93061371" : "Kenna, N.M.", "sn83045030" : "Albuquerque, N.M.", "sn83045398" : "Taos, N.M.", "sn93061743" : "Taos, N.M.", "sn94056834" : "Taos, N.M.", "sn83045436" : "Santa Fe, N.M.", "sn93061467" : "Estancia, N.M.", "sn90051703" : "Las Vegas, N.M.", "sn86063592" : "Las Vegas, N.M.", "sn96061021" : "Las Vegas, N.M.", "sn84027457" : "Las Vegas, N.M.", "sn93061633" : "Las Vegas, N.M.", "sn93061631" : "Las Vegas, N.M.", "sn92070417" : "Las Vegas, N.M.", "sn92070422" : "Las Vegas, N.M.", "sn87090072" : "White Oaks, N.M.", "sn91052379" : "Cerrillos, N.M.", "sn94005878" : "Lovington, N.M.", "sn84027433" : "Mesilla, N.M.", "sn87090075" : "Mesilla, N.M.", "sn93061497" : "Mesilla, N.M.", "sn84020617" : "Albuquerque, N.M.", "sn92070567" : "Estancia, N.M.", "sn93061704" : "Mountainair, N.M.", "sn84024881" : "Santa Fe, N.M.", "sn93061701" : "Santa Fe, N.M.", "sn930617407" : "White Oaks, N.M.", "sn93061752" : "Raton, N.M.", "sn91052387" : "Raton, N.M.", "sn91052388" : "Raton, N.M.", "sn92070553" : "Red River, N.M.", "sn93061795" : "Reserve, N.M.", "sn87090080" : "Las Cruces, N.M.", "sn86063823" : "Roswell, N.M.", "sn92072386" : "Cerrillos, N.M.", "sn93061544" : "San Jon, N.M.", "sn92070446" : "Aztec, N.M.", "sn86063590" : "Farmington, N.M.", "sn84020631" : "Santa Fe, N.M.", "sn88071076" : "Santa Fe, N.M.", "sn88071075" : "Santa Fe, N.M.", "sn84022168" : "Santa Fe, N.M.", "sn84022165" : "Santa Fe, N.M.", "sn84020630" : "Santa Fe, N.M.", "sn84020626" : "Santa Fe, N.M.", "sn94057006" : "Kingston, N.M.", "sn92070455" : "Socorro, N.M.", "sn86090503" : "Socorro, N.M.", "sn86090456" : "Silver City, N.M.", "sn92061524" : "Roy, N.M.", "sn94057002" : "Taiban, N.M.", "sn93061711" : "Tucumcari, N.M.", "sn93061709" : "Tucumcari, N.M.", "sn87067095" : "Santa Fe, N.M.", "sn87067094" : "Santa Fe, N.M.", "sn92070405" : "Lordsburg, N.M.", "sn87090065" : "White Oaks, N.M."}