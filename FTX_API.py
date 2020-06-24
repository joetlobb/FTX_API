import ccxt, json, pandas

ftx = ccxt.ftx({
    'apiKey': 'api_key' ,
    'secret': 'api_secret' })

##This is main account
##ftx.headers = {
##    'FTX-SUBACCOUNT': 'BTC01 Trend',}

while True:
    print('What do you want to do?',
          '\n\n0 Get Price Data\n1 Check Balance\n2 Open order',
          '\n3 Check position\n4 Check pending order',
          '\n5 Cancel order\n6 Check Trade History')

    toDO=input()
    if int(toDO)==0:
        print("Symbol?", ftx.symbols)
        symbol=input()
        r = json.dumps(ftx.fetch_ticker(symbol))
        dataPrice = json.loads(r)
        print(symbol, ':', dataPrice['last'],'\n')

    elif int(toDO)==1:
        balance = ftx.fetch_balance()
        df = pandas.DataFrame(data=balance, columns = ['free','used','total'])
        print('     *** Wallet balance ***\n')
        print(df,'\n')

    elif int(toDO)==2:
        print('Open order which Symbol?')
        pair = input()
        while True:
            print('Open order buy or sell?')
            side = input()
            if side == 'buy' or side == 'sell':
                break
        print('Open order size in pair(BTC,XRP) not USD')
        size_order=input()
        print('At price?')
        price=input()
        respond = ftx.create_order(pair, 'limit' , side, size_order, price)
        df = pandas.DataFrame(data=respond)
        print(df[['info']],'\n')

    elif int(toDO)==3:
        data=ftx.fetch_trading_fees()['info']
        df = pandas.DataFrame(data)
        print(df.drop(index=['backstopProvider','chargeInterestOnNegativeUsd',
                             'positionLimit','positionLimitUsed',
                             'spotLendingEnabled','spotMarginEnabled',
                             'useFttCollateral',
                             'initialMarginRequirement',
                             'liquidating','username','positions'],
                              columns=['success']).rename(columns={"result": "Account status"}))
        df2 = pandas.DataFrame(data['result']['positions'], index=['Positions [0]'],
                               columns=['future','side','netSize','cost',
                                        'estimatedLiquidationPrice',
                                        'entryPrice'])
        print(df2.transpose(),'\n')
        myTrades=ftx.fetchMyTrades()
##        print(myTrades[19])
##        print(pandas.DataFrame(myTrades[19]).transpose())
        print('Enter size of position to calculate PnL')
        sizeOfOrder = float(input())
        for a in reversed(myTrades):
            if a['amount'] == sizeOfOrder:
                print('\nList of trades with size of', sizeOfOrder,
                      '\n\nIndex of trade no.',myTrades.index(a))
                df3=pandas.DataFrame(a, columns=['info'])
                print(df3.loc[['market','side','size','price','time']])
        print('\nWhich trade number to calculate PnL?')
        orderNumber=input()
        openPrice = myTrades[int(orderNumber)]['price']
        r = json.dumps(ftx.fetch_ticker(data['result']['positions'][0]['future']))
        dataPrice = json.loads(r)
        marketPrice = dataPrice['last']
        print(df2.transpose(),'\n')
        print('PnL ', sizeOfOrder*(marketPrice-openPrice),'\n')

    elif int(toDO)==4:
        df = pandas.DataFrame(ftx.fetch_open_orders(),columns=['id','datetime','symbol','side','price','amount'])
        print('     *** Pending open orders ***\n')
        print(df,'\n')
        
    elif int(toDO)==5:
        openOrders=ftx.fetch_open_orders()
        print('Type order number in pending list to cancel.')
        cancelNo=input()
        respond=ftx.cancel_order(openOrders[int(cancelNo)]['id'])
        print(respond,'\n')

    elif int(toDO)==6:
        data=ftx.fetchMyTrades()
        print(pandas.DataFrame(data[6]))
        print(pandas.DataFrame(data[6]).transpose())

