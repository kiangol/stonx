import csv
import pandas as pd
from asset import Asset
from portfolio import Portfolio

# filename = input("Drag and drop the file (or type the filename): ")
filename = 'transactions_2.csv'
# f = open(filename, 'r', encoding='utf-16')
#
#
# for line in f:
#     print(line)
columns = ['Verdipapir', 'Transaksjonstype', 'Antall', 'Kurs', 'Beløb', 'Kjøpsverdi', 'Resultat', 'Vekslingskurs']
df = pd.read_csv(filename, usecols=columns, delimiter='\t', encoding='utf-16')
print(df.to_string())

pf = Portfolio()
for index, row in df.iterrows():
    ticker = row['Verdipapir']
    amount = float(row['Antall'].replace(',', '.').replace(' ', ''))
    kurs = float(row['Kurs'].replace(',', '.').replace(' ', ''))
    vekslingskurs = float(row['Vekslingskurs'].replace(',', '.').replace(' ', ''))
    transaksjonstype = row['Transaksjonstype']
    belop = float(row['Beløb'].replace(',', '.').replace(' ', ''))

    if transaksjonstype == 'KJØPT' or transaksjonstype == 'SALG':
        a = Asset(ticker)
        pf.add_asset(a)
        pf_asset = pf.get_asset(ticker)
        pf_asset.buy(amount, kurs * vekslingskurs) if belop > 0 else pf_asset.sell(amount, kurs * vekslingskurs)

    if transaksjonstype == 'INNSKUDD' or transaksjonstype == 'UTTAK INTERNET':
        if transaksjonstype == 'INNSKUDD':
            print(f"DEPOSIT: {belop}")
            pf.deposit(belop)

for a in pf.get_assets():
    print(a)

print(pf)
