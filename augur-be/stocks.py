from flask import Blueprint, g
import yfinance as yf
import os.path as path
from random import randint
from .models import db, Stock
from .middlewares import authMiddleware
import json

bp = Blueprint('stocks', __name__)
baseDir = path.abspath(path.dirname('__file__'))


@bp.route('/explore')
@authMiddleware
def explore():
    with open(path.join(baseDir, 'augur-be', 'symbols.txt')) as reader:
        allSymbols = list(reader)

    # usedSymbols = getUsedSymbols(allSymbols)
    data = yf.download(' '.join(allSymbols), period="2d", group_by="ticker")

    return {'data': transformData(data, allSymbols)}


@bp.route('/stock/view/<string:symbol>')
@authMiddleware
def view(symbol):
    ticker = yf.Ticker(symbol)
    stock = Stock.query.filter((Stock.symbol == symbol) & (
        Stock.user_id == g.user_id)).first()
    following = True

    if stock is None:
        following = False

    return {'data': ticker.info, 'following': following}


@bp.route('/follow/<string:symbol>')
@authMiddleware
def follow(symbol):
    stock = Stock(symbol=symbol, user_id=g.user_id)
    db.session.add(stock)
    db.session.commit()

    return {'data': 'Followed Successfully'}


@bp.route('/unfollow/<string:symbol>')
@authMiddleware
def unfollow(symbol):
    stock = Stock.query.filter((Stock.symbol == symbol) & (
        Stock.user_id == g.user_id)).first()
    db.session.delete(stock)
    db.session.commit()

    return {'data': 'Unfollowed Successfully'}


@bp.route('/stock/followed')
@authMiddleware
def followedStocks():
    stocks = Stock.query.filter((Stock.user_id == g.user_id)).all()
    symbols = []

    for stock in stocks:
        symbols.append(stock.symbol)

    data = yf.download(' '.join(symbols), period="2d", group_by="ticker")

    return {'data': transformData(data, symbols)}


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


def transformData(data, symbols):
    information = []

    for symbol in symbols:
        if len(symbols) > 1:
            information.append(createStockObject(data, symbol))
        else:
            information.append(createSingleStockObject(data, symbol))

    return information


def createStockObject(data, symbol):
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

    return stock


def createSingleStockObject(data, symbol):
    stock = dict()
    stock['symbol'] = symbol.replace("\n", "")
    stock['open'] = data['Open'][1]
    stock['close'] = data['Close'][1]
    stock['high'] = data['High'][1]
    stock['low'] = data['Low'][1]

    priceChange = data['Close'][1] - data['Close'][0]

    if priceChange > 0:
        stock['direction'] = 'up'
    else:
        stock['direction'] = 'down'

    stock['priceChange'] = priceChange

    return stock
