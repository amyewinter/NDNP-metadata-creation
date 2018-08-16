from PyPDF2 import PdfFileMerger

pdfs = ['animal-smiley-faces.pdf', 'greatday.pdf']

pdfname = "C:\\Users\\amywinter\\Desktop\\newspapers test\\test-07-27-2018-combined.pdf"

merger = PdfFileMerger()

for pdf in pdfs:
	merger.append(open(pdf, 'rb'))
	
with open(pdfname, 'wb') as fout:
	merger.write(fout)