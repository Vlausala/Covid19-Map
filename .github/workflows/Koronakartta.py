import requests
import pygal
import webbrowser as wb
from pygal.style import Style
url = "https://api.thevirustracker.com/free-api?countryTotals=ALL"

class MAA:
	nimi=""
	maakoodi =""
	total_cases=""
	recovered=""
	deaths=""

def paaohjelma():
	maatiedot = []

	maat = haetiedot(url)
	maatiedot = formatoi(maat)
	kartoita(maatiedot)
	
	return None################################################################
	
def haetiedot(url):
	'''Hakee maatiedot corona-apista'''
	r = requests.get(url) #Tekee request objektin 
	resp_dict = r.json() #Tekee dictionaryn request objektista
	maat = resp_dict["countryitems"] #Tekee listan, jossa kaksi elementtiä
	maat = maat[0] #Tekee dictionaryn listan elementistä.
	return maat

def formatoi(maat):
	"""Tekee listan MAA-objekteja"""
	maalista = []
	for value in maat.values():
		try:
			maatieto = MAA()
			maatieto.nimi = value["title"]
			maatieto.maakoodi = value["code"].lower()
			maatieto.total_cases = int(value["total_cases"])
			maatieto.recovered = int(value["total_recovered"])
			maatieto.deaths = int(value["total_deaths"])
			maalista.append(maatieto)
			print("Maa ladattu:",value["title"])
		except:
			continue
	return maalista

def kartoita(maatiedot):
	"""Piirtää koronakartan maatietojen perusteella"""
	
	print("\nMistä olet kiinnostunut?")
	print("1) Tapausten määrä\n2) Parantuneiden määrä\n3) Kuolleiden määrä")
	while True:
		try:
			vastaus=int(input("Vastaukseni: "))
			if 1 <= vastaus <= 3:
				break
		except:
			continue	

	if vastaus == 1:
		custom_style = Style(colors=('#00FF00', '#FFFF00', '#FF0000'), font="arial")
		wm = pygal.maps.world.World(style=custom_style) #Luo worldmap objektin
		wm.title = "Koronatapausten määrä maailmalla (Lähde: thevirustracker.com)"
		ryhma1, ryhma2, ryhma3 = {},{},{}

		#Sortataan tapaukset ryhmittäin niiden määrän mukaan
		for rivi in maatiedot:
			if rivi.total_cases < 1000:
				ryhma1[rivi.maakoodi] = rivi.total_cases
			elif 1000 < rivi.total_cases <= 10000:
				ryhma2[rivi.maakoodi] = rivi.total_cases
			elif rivi.total_cases > 10000:
				ryhma3[rivi.maakoodi] = rivi.total_cases

		wm.add("<1000", ryhma1)
		wm.add("1000-10000",ryhma2)
		wm.add("10000<",ryhma3)
		wm.render_to_file('Koronakartta.svg')
		print("Koronakartta.svg tallennettu.")
		wb.open_new_tab("Koronakartta.svg")
		return None
	elif vastaus == 2:
		custom_style = Style(colors=('#FF0000', '#FFFF00', '#00FF00'), font="arial")
		wm = pygal.maps.world.World(style=custom_style) #Luo worldmap objektin
		wm.title = "Koronasta parantuneiden määrä maailmalla (Lähde: thevirustracker.com)"
		ryhma1, ryhma2, ryhma3 = {},{},{}

		#Sortataan tapaukset ryhmittäin niiden määrän mukaan
		for rivi in maatiedot:
			if rivi.recovered < 1000:
				ryhma1[rivi.maakoodi] = rivi.recovered
			elif 1000 < rivi.total_cases <= 10000:
				ryhma2[rivi.maakoodi] = rivi.recovered
			elif rivi.total_cases > 10000:
				ryhma3[rivi.maakoodi] = rivi.recovered

		wm.add("<1000", ryhma1)
		wm.add("1000-10000",ryhma2)
		wm.add("10000<",ryhma3)
		wm.render_to_file('Koronakartta.svg')
		print("Koronakartta.svg tallennettu.")
		wb.open_new_tab("Koronakartta.svg")
		return None

	elif vastaus == 3:
		custom_style = Style(colors=('#00FF00', '#FFFF00', '#FF0000'), title_font_family="arial")
		wm = pygal.maps.world.World(style=custom_style) #Luo worldmap objektin
		wm.title ="Koronaan kuolleiden määrä maailmalla (Lähde: thevirustracker.com)"
		ryhma1, ryhma2, ryhma3 = {},{},{}

		#Sortataan tapaukset ryhmittäin niiden määrän mukaan
		for rivi in maatiedot:
			if rivi.deaths < 100:
				ryhma1[rivi.maakoodi] = rivi.deaths
			elif 100 < rivi.deaths <= 1000:
				ryhma2[rivi.maakoodi] = rivi.deaths
			elif rivi.deaths > 1000:
				ryhma3[rivi.maakoodi] = rivi.deaths

		wm.add("<100", ryhma1)
		wm.add("100-1000",ryhma2)
		wm.add("1000<",ryhma3)
		wm.render_to_file('Koronakartta.svg')
		print("Koronakartta.svg tallennettu.")
		wb.open_new_tab("Koronakartta.svg")
		return None



paaohjelma()



###############################EOF#############################################
