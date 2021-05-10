import re

from flask import Flask, render_template, request, redirect
from portfolio import Portfolio
from asset import Asset
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    import os
    if not os.path.exists('transaction_files'):
        os.makedirs('transaction_files')
    return render_template('index.html', content="Welcome to StonX!")

@app.route('/help')
def help():
    return render_template('help.html')


app.config["UPLOAD_DIR"] = '/Users/kian/PycharmProjects/stonx/static/csv/uploads'
app.config["ALLOWED_EXT"] = ['CSV', 'TXT']


def allowed_filetype(filename):
    """Checks if the uploaded filetype is allowed

    Args:
        filename (str): the complete filename

    Returns:
        boolean: True if file is allowed, else False
    """
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1]
    return ext.upper() in app.config["ALLOWED_EXT"]


def create_portfolio(data):
    print("CREATING PORTFOLIO")
    pf = Portfolio()

    for index, row in data.iterrows():
        ticker = row['Verdipapir']
        amount = float(row['Antall'].replace(',', '.').replace(' ', ''))
        kurs = float(row['Kurs'].replace(',', '.').replace(' ', ''))
        vekslingskurs = float(row['Vekslingskurs'].replace(',', '.').replace(' ', ''))
        transaksjonstype = row['Transaksjonstype']
        belop = float(row['Beløb'].replace(',', '.').replace(' ', ''))

        # Deposit and withdraw cash
        if transaksjonstype == 'INNSKUDD' or transaksjonstype == 'UTTAK INTERNET':
            if transaksjonstype == 'INNSKUDD':
                pf.deposit(belop)
            if transaksjonstype == 'UTTAK INTERNET':
                pf.withdraw(belop)

        if transaksjonstype == 'KJØPT' or transaksjonstype == 'SALG':
            a = Asset(ticker)
            pf.buy(a, amount, (kurs * vekslingskurs)) if belop < 0 else pf.sell(a, amount, (kurs * vekslingskurs))

    return pf


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not request.files.get('uploaded_file', None):
            return render_template('index.html',
                                   errormsg="Ingen fil valgt, velg fil først")
        if request.files:

            file_uploaded = request.files['uploaded_file']

            if file_uploaded.filename == "":
                print("FILENAME ERROR")
                return redirect(request.url)

            if not allowed_filetype(file_uploaded.filename):
                print("Filetype is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(file_uploaded.filename)
                dir1 = os.getcwd()
                target_dir = dir1 + '/transaction_files'
                file_uploaded.save(os.path.join(target_dir, filename))

            columns = ['Handelsdag', 'Transaksjonstype', 'Antall', 'Verdipapir', 'Kurs', 'Beløb', 'Kjøpsverdi', 'Resultat',
                       'Vekslingskurs']
            df = pd.read_csv(os.path.join(target_dir, filename), usecols=columns, delimiter='\t',
                             encoding='utf-16')

            df = df.iloc[::-1]

            pf = create_portfolio(df)

            df_html = df.to_html(index=False, justify='left', col_space='1px', na_rep='')
            html_table = re.sub('border=\"1\" class=\"dataframe\"',
                                'class=\"table table-bordered table-dark table-hover\"',
                                df_html)

            return render_template('upload.html',
                                   status=f"Uploaded {filename}",
                                   tables=[html_table],
                                   titles=df.columns.values,
                                   total_value=f"{pf.get_portfolio_value():.2f} NOK",
                                   deposits=f"{sum(pf.deposits)}",
                                   withdrawals=f"{abs(sum(pf.withdrawals))}",
                                   )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
