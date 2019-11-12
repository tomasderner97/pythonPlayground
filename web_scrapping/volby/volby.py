import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup

os.chdir(r"C:\Users\tomas\Repositories\pythonplayground\volby\vysledky")
html = open("1517057939.html", "r").read()
soup = BeautifulSoup(html, "html.parser")
okrsky_sectene = soup.find(headers="r12 s1a1 s1b2").contents[0]
okrsky_procenta = soup.find(headers="r12 s1a1 s1b3").contents[0]

