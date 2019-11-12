import PyPDF2 as pdf
import os

SONGS_PATH = "C:/Users/tomas/zpevnik"

paths = sorted(os.listdir(SONGS_PATH))
paths.insert(39, paths.pop())  # hack: dá Čechomor na správné místo v abecedě

files = [open(os.path.join(SONGS_PATH, path), "rb") for path in paths]

output = pdf.PdfFileWriter()

for i, (file, f) in enumerate(zip(paths, files)):
    print(f"Working on {i}: ", end=" ")
    page = pdf.PdfFileReader(f)
    output.addPage(page.getPage(0))

    page_name = os.path.splitext(os.path.basename(file))[0]
    print(page_name)

    output.addBookmark(page_name, i)

with open("out.pdf", "wb") as f:
    output.write(f)
