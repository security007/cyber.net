from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, Response
from v1 import api
from urllib.parse import unquote, urlparse, urlunparse, quote, quote_plus
import requests
import base64


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def about():
    __version = "1.0.0"
    __author = "security007"
    __email = "defacementsec007@gmail.com"
    return {'version': __version, 'author': __author, 'email': __email}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', about=about())


@app.route('/cari', methods=['GET'])
def cari():
    carikan = api.Garuda()
    kata = request.args.get('kata')
    nextPrev = request.args.get('nextPrev')
    if nextPrev != None:
        dec = base64.b64decode(nextPrev)
        res = carikan.scrap(
            customPage=dec.decode())
    else:
        res = carikan.scrap(query=kata)
    jumlah = len(res['results'])
    return render_template('cari.html', about=about(), hasil=res, jumlah=jumlah, kata=quote_plus(quote(kata, safe="")), kataplaceholder=unquote(kata))


@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['domain']
    carikan = api.Garuda()
    res = carikan.scan(url)
    return {'hasil': str(res)}


# if __name__ == '__main__':
#     app.run(debug=True)
