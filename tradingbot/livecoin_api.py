# -*- coding: utf-8 -*-codung
import httplib
import urllib
import json
import hashlib
import hmac
from collections import OrderedDict
from collections import namedtuple
import config
import time
import support
import database
def delete_after(result):
    return " ".join(map(str, set(result)))

def get_data(method, *args):
    """
    :param method: 
    :param args: 
    :return: 
    """
    time.sleep(1)

    server = config.API_URl
    keys = support.get_keys()
    api_key = keys[0]
    secret_key = keys[1]


    data = OrderedDict(args)

    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg=encoded_data,
                    digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign}

    conn = httplib.HTTPSConnection(server)
    conn.request("GET", method + '?' + encoded_data, '', headers)

    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data


def post_data(method, *args):
    """

    :param method: 
    :param args: 
    :return: 
    """
    time.sleep(1)
    server = config.API_URl
    keys = support.get_keys()
    api_key = keys[0]
    secret_key = keys[1]

    data = OrderedDict(args)
    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg=encoded_data,
                    digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign,
               "Content-type": "application/x-www-form-urlencoded"}

    conn = httplib.HTTPSConnection(server)
    conn.request("POST", method, encoded_data, headers)
    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data

def get_exchange_ticker(*args):

    """
    Получить информацию за последние 24 часа по конкретной паре валют.
    В ответе есть следующие поля:
        max_bid, min_ask - максимальный бид и минимальный аск за последние 24 часа
        best_bid, best_ask - лучшие текущие бид и аск
    :param args: 
    :return: 
    """
    result = get_data("/exchange/ticker",*args)
    if len(args):
        result = [result]

    Exchange_ticker = namedtuple("Exchange_ticker", "%s"%delete_after(result[
                                                                          0]))

    return map(lambda x: Exchange_ticker(**x),result)


def get_exchange_last_trades(currencyPair, *args):
    """
    Получить информацию о последних сделках (транзакциях) по заданной паре валют.
    Информацию можно получить либо за последний час либо за последнюю минуту.
    
    :param currencyPair: 
    :param args: 
    :return: 
    """

    result = get_data("/exchange/last_trades",("currencyPair",
                                               currencyPair),*args)

    Exchange_last_trades = namedtuple("Exchange_last_trades", "%s"
                                      % delete_after(result[0]))

    return map(lambda x: Exchange_last_trades(**x), result)


def get_exchange_order_book(currencyPair, *args):
    """
    Получить ордера по выбранной паре (можно установить признак
     группировки ордеров по ценам)
    :param currencyPair: 
    :param args: 
    :return: 
    """
    result = get_data("/exchange/order_book", ("currencyPair",
                                                currencyPair), *args)

    Exchange_order_book = namedtuple("Exchange_order_book", "%s"
                                      % delete_after(result))

    return map(lambda x: Exchange_order_book(**x), [result])

#problem
def get_exchange_all_order_book(*args):
    """
    Возвращает ордербук по каждой валютной паре
    :param args: 
    :return: 
    """
    pass


def get_exchange_maxbid_minask(*args):
    """
    Возвращает максимальный бид и минимальный аск в текущем стакане
    :param args: 
    :return: 
    """
    pass

def get_exchange_restrictions(*args):
    """
    Возвращает ограничения по каждой паре по мин. размеру ордера и максимальному
     кол-ву знаков после запятой в цене.
    :param args: 
    :return: 
    """
    pass

def get_info_coinInfo(*args):
    """
    возвращает общую информацию по критовалютам:
        name - название
        symbol - символ
        walletStatus - статус кошелька
        normal - Кошелек работает нормально
        delayed - Кошелек задерживается (нет нового блока 1-2 часа)
        blocked - Кошелек не синхронизирован (нет нового блока минимум 2 часа)
        blocked_long - Последний блок получен более 24 ч. назад
        down - Кошелек временно выключен
        delisted - Монета будет удалена с биржи, заберите свои средства
        closed_cashin - Разрешен только вывод
        closed_cashout - Разрешен только ввод
        withdrawFee - комиссия вывод
        minDepositAmount - мин. сумма пополнения
        minWithdrawAmount - мин. сумма вывода
    :param args: 
    :return: 
    """
    pass

def get_exchange_trades(*args):
    """
    По конкретному клиенту получить информацию о его последних сделках,
     результат может быть ограничен, соответствующими параметрами.
    :param args: 
    :return: 
    """

    result = get_data("/exchange/trades",*args)
    if len(args):
     result = [result]

    Exchange_trades = namedtuple("Exchange_trades", "%s"%delete_after(result[
                                                                       0]))

    return map(lambda x: Exchange_trades(**x),result)

#сложно взаимодействие с системой
def get_exchange_client_orders(*args):
    """
    По конкретному клиенту и по конкретной паре валют получить полную информацию
     о его ордерах, информация может быть ограничена
     либо только открытые либо только закрытые ордера.
    :param args: 
    :return: 
    """
    pass

def get_exchange_order(orderId):
    """
    Получить информацию об ордере по его ID
    :param orderId: 
    :return: 
    """
    result = get_data("/exchange/trades", ("ordeId",orderId))

    Exchange_order = namedtuple("Exchange_order", "%s" % delete_after(result[
                                                                            0]))

    return map(lambda x: Exchange_order(**x), [result])


def get_payment_balances(*args):
    """
    Возвращает массив с балансами пользователя. Для каждой валюты существует
    4 типа балансов: общий (total),
    доступные для торговли средства (available),
    средства в открытых ордерах (trade),
    доступный для вывода (available_withdrawal)
    :param args: 
    :return: 
    """
    result = get_data("/payment/balances", *args)

    Payment_balances = namedtuple("Payment_balances", "%s" % delete_after(result[
                                                                          0]))

    return map(lambda x: Payment_balances(**x), result)

def get_payment_balance(currency):
    """
    Возвращает доступный баланс для выбранной валюты
    :param args: 
    :return: 
    """
    result = get_data("/payment/balances", ("currency",currency))

    Payment_balance = namedtuple("Payment_balance",
                                  "%s" % delete_after(result[0]))

    return map(lambda x: Payment_balance(**x), result)

#todo
def get_payment_history_transactions(start, end, *args):
    """
    Возвращает список транзакций пользователя
    :param start: 
    :param end: 
    :return: 
    """
    result = get_data(" /payment/history/transactions", ("start", start),
                      ("end",end))
    print result
    Payment_history_transactions = namedtuple("Payment_history_transactions",
                                 "%s" % delete_after(result[0]))

    return map(lambda x: Payment_history_transactions(**x), result)
#todo
def get_payment_history_size(start, end, *args):
    """
    Возвращает количество транзакций пользователя с заданными параметрами
    :param start: 
    :param end: 
    :param args: 
    :return: 
    """
    pass

def get_exchange_commission():
    """
    Возвращает текущую комиссию пользователя
    :return: 
    """
    result = get_data("/exchange/commission",)
    print result
    Payment_history_transactions = namedtuple("Payment_history_transactions",
                                              "%s" % delete_after(result))

    return map(lambda x: Payment_history_transactions(**x), [result])

def get_exchange_commissionCommonInfo():
    """
    Возвращает текущую комиссию пользователя
     и объем торгов в USD за последние 30 дней
    :return: 
    """

    result = get_data("/exchange/commissionCommonInfo", )
    Exchange_commissionCommonInfo = namedtuple("Payment_history_transactions",
                                              "%s" % delete_after(result))

    return map(lambda x: Exchange_commissionCommonInfo(**x), [result])

def post_exchange_buylimit(currencyPair, price, quantity):
    """
    Открыть ордер (лимитный) на покупку, определенной валюты.
    :param currencyPair: 
    :param price: 
    :param quantity: 
    :return: 
    """
    result = post_data("/exchange/buylimit",("currencyPair",currencyPair),
                    ("price",price),("quantity",quantity))
    Post_exchange_buylimit = namedtuple("Post_exchange_buylimit",
                                              "%s" % delete_after(result))

    return map(lambda x: Post_exchange_buylimit(**x), [result])

def post_exchange_selllimit(currencyPair, price, quantity):
    """
    Открыть ордер (лимитный) на продажу определенной валюты. 
    Доп.параметры аналогично покупки.

    :param currencyPair: 
    :param price: 
    :param quantity: 
    :return: 
    """
    result = post_data("/exchange/selllimit", ("currencyPair", currencyPair),
                       ("price", price), ("quantity", quantity))
    Post_exchange_selllimit= namedtuple("Post_exchange_buylimit",
                                        "%s" % delete_after(result))

    return map(lambda x: Post_exchange_selllimit(**x), [result])

def post_exchange_buymarket(currencyPair, quantity):
    """
    Открыть ордер(рыночный) на покупку определенной валюты на заданное количество.
    :return: 
    """
    result = post_data("/exchange/buymarket", ("currencyPair", currencyPair),
                         ("quantity", quantity))
    Post_exchange_buymarket = namedtuple("Post_exchange_buylimit",
                                         "%s" % delete_after(result))

    return map(lambda x: Post_exchange_buymarket(**x), [result])

def post_exchange_sellmarket(currencyPair, quantity):
    """
    Открыть ордер(рыночный) на продажу определенной валюты на заданное количество.
    :param currencyPair: 
    :param quantity: 
    :return: 
    """

    result = post_data("/exchange/sellmarket", ("currencyPair", currencyPair),
                       ("quantity", quantity))
    Post_exchange_sellmarket = namedtuple("Post_exchange_sellmarket",
                                         "%s" % delete_after(result))

    return map(lambda x: Post_exchange_sellmarket(**x), [result])

def post_exchange_cancellimit(currencyPair, orderId):
    """
    Отменить ордер (лимитный).
    :param currencyPair: 
    :param orderId: 
    :return: 
    """
    result = post_data("/exchange/cancellimit", ("currencyPair", currencyPair),
                       ("orderId", orderId))
    Post_exchange_cancellimit = namedtuple("Post_exchange_cancellimit",
                                          "%s" % delete_after(result))

    return map(lambda x: Post_exchange_cancellimit(**x), [result])
