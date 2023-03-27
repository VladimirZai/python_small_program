from PyPDF2 import PdfFileWriter, PdfFileReader
from getpass import getpass

# Защита пдф файла паролем
pdffile = PdfFileWriter()
pdf = PdfFileReader('Profile.pdf')

for page in range(pdf.numPages):
    pdffile.add_page(pdf.pages[page])

password = getpass(prompt='Enter password:')
pdffile.encrypt(password)

with open('protected.pdf', 'wb') as file:
    pdffile.write(file)

