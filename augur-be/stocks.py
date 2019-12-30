from flask import Blueprint
import yfinance as yf
import os.path as path
from random import randint
import json

bp = Blueprint('stocks', __name__)
baseDir = path.abspath(path.dirname('__file__'))


@bp.route('/explore')
def explore():
    with open(path.join(baseDir, 'augur-be', 'symbols.txt')) as reader:
        allSymbols = list(reader)

    usedSymbols = getUsedSymbols(allSymbols)
    data = yf.download(' '.join(usedSymbols), start="2019-12-27",
                       end="2019-12-28", group_by="ticker")

    return {'data': transformData(data, usedSymbols)}


@bp.route('/stock/view/<string:symbol>')
def view(symbol):
    ticker = yf.Ticker(symbol)

    return {'info': ticker.info}



# obtaining the 15 symbols to be displayed
def getUsedSymbols(allSymbols):
    i = 0
    usedSymbols = []
    while i < 10:
        value = randint(0, len(allSymbols) - 1)

        if allSymbols[value] not in usedSymbols:
            usedSymbols.append(allSymbols[value])
            i += 1

    return usedSymbols



def transformData(data, usedSymbols):
    information = []

    for symbol in usedSymbols:
        stock = dict()
        stock['symbol'] = symbol.replace("\n", "")
        stock['open'] = data[symbol.replace("\n", "")]['Open'][1]
        stock['close'] = data[symbol.replace("\n", ""), 'Close'][1]
        stock['high'] = data[symbol.replace("\n", ""), 'High'][1]
        stock['low'] = data[symbol.replace("\n", ""), 'Low'][1]

        priceChange = data[symbol.replace(
            "\n", "")]['Close'][1] - data[symbol.replace("\n", "")]['Close'][0]

        if priceChange > 0:
            stock['direction'] = 'up'
        else:
            stock['direction'] = 'down'

        stock['priceChange'] = priceChange
        information.append(stock)

    return information
