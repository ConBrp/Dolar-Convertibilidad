# -*- coding: utf-8 -*-
import pdfplumber
import requests
from bs4 import BeautifulSoup

# URL del PDF a descargar, Informe diario del BCRA.
url = "https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/infomondiae.pdf"

# Descarga el archivo PDF.
response = requests.get(url)

# Guarda el archivo en disco.
with open("example.pdf", "wb") as f:
    f.write(response.content)

# Se busca el precio de venta del dólar blue en una página reconocida.
response = requests.get("https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB")
soup = BeautifulSoup(response.text, "html.parser")
dolar_blue = soup.find_all("div", "sell-value")[0].text
blue_dolar = float(dolar_blue[1:].replace(".", "").replace(",", "."))

# Se busca el precio de venta del dólar oficial en el Banco Nación de la República Argentina.
response = requests.get("https://www.bna.com.ar/Personas")
soup = BeautifulSoup(response.text, "html.parser")
precio = soup.find_all("table", "table cotizacion")
precio = precio[0].find_all("td")
BNA = float(precio[2].text.replace(",", "."))


# Abre el archivo PDF con pdfplumber y extrae las tablas.
with pdfplumber.open("example.pdf") as pdf:
    page = pdf.pages
    tables = page[3].extract_tables()[0]

    base_monetaria = float(tables[22][0].split()[2].replace(",", ""))
    leliqs = float(tables[26][0].split()[4].replace(",", ""))
    legar = float(tables[28][0].split()[4].replace(",", ""))
    pases = float(tables[30][0].split()[2].replace(",", ""))
    reservas = float(tables[36][0].split("\n")[-2].split()[3].replace(",", ""))
    fecha = tables[20][2]
    fecha_real = tables[0][0]

    agregado1 = base_monetaria + leliqs + legar + pases
    agregado2 = base_monetaria + leliqs
    agregado3 = base_monetaria + legar + pases

    tables = page[4].extract_tables()[-1]
    M3 = float(tables[34][0].split()[-11].replace(",", ""))
    M2 = float(tables[33][0].split()[-9].replace(",", ""))
    M1 = float(tables[32][0].split()[-11].replace(",", ""))

    # Se imprimen por pantalla los resultados.
    print(fecha_real + f"  --  Saldos al {fecha}")
    print()
    print(f"Dólar de convertibilidad = $ {agregado1 / reservas:.2f}")
    print(f"Diferencia contra blue = $ {agregado1 / reservas - blue_dolar:.2f}  {((agregado1 / reservas - blue_dolar) / blue_dolar * 100):.2f} %")
    print()
    print(f"Dólar Blue = $ {blue_dolar}")
    print()
    print(f"Dólar \"BNA\" = $ {agregado3/reservas:.2f}")
    print(f"Dólar BNA = $ {BNA}")
    print(f"Diferencia = $ {agregado3/reservas-BNA:.2f}  {((agregado3/reservas-BNA) / BNA) * 100:.2f} %")

    print()
    print(f"Dólar \"BANCOS\" = $ {agregado2/reservas:.2f}")
    print()
    print(f"Multiplicador (M1): {M1/base_monetaria:.2f}")
    print(f"Multiplicador (M2): {M2/base_monetaria:.2f}")
    print(f"Multiplicador (M3): {M3/base_monetaria:.2f}")
    print()
    print(f"Pasivos remunerados en términos de la BM: {(agregado1-base_monetaria)/base_monetaria:.2f} veces")
    print()
    print(f"Base Monetaria = $ {base_monetaria:_.0f}")
    print(f"Leliqs = $ {leliqs:_.0f}")
    print(f"Otras letras = $ {legar:_.0f}")
    print(f"Pases pasivos = $ {pases:_.0f}")
    print(f"Reservas = U$S {reservas:_.0f}")


