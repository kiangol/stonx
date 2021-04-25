from flask import Flask, render_template, request, redirect
from portfolio import Portfolio
from asset import Asset
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', content="Welcome to StonX!")


app.config["UPLOAD_DIR"] = '/Users/kian/PycharmProjects/stonx/static/csv/uploads'
app.config["ALLOWED_EXT"] = ['CSV', 'TXT']


def allowed_filetype(filename):
    """Checks if the uploaded filetype is allowed

    Args:
        filename (str): the complete filename

    Returns:
        boolean: True if file is allowed, else False
    """

    if not '.' in filename:
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

        if transaksjonstype == 'KJØPT' or transaksjonstype == 'SALG':
            a = Asset(ticker)
            pf.add_asset(a)
            pf_asset = pf.get_asset(ticker)
            pf_asset.buy(amount, kurs * vekslingskurs) if belop < 0 else pf_asset.sell(amount, kurs * vekslingskurs)

        if transaksjonstype == 'INNSKUDD' or transaksjonstype == 'UTTAK INTERNET':
            if transaksjonstype == 'INNSKUDD':
                print(f"DEPOSIT: {belop}")
                pf.deposit(belop)

        return pf


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
                file_uploaded.save(os.path.join(app.config['UPLOAD_DIR'], filename))


            columns = ['Verdipapir', 'Transaksjonstype', 'Antall', 'Kurs', 'Beløb', 'Kjøpsverdi', 'Resultat', 'Vekslingskurs']
            filename = 'transactions.csv'
            df = pd.read_csv(os.path.join(app.config['UPLOAD_DIR'], filename), usecols=columns, delimiter='\t', encoding='utf-16')

            pf = create_portfolio(df)

            return render_template('upload.html',
                                   status=f"Uploaded {filename}",
                                   tables=[df.to_html(classes='data')],
                                   titles=df.columns.values,
                                   total_value=pf.get_equity()
                                   )
            # return redirect(request.url)
    # return df.to_html()


if __name__ == '__main__':
    app.run(debug=True, port=1312)
