import sqlite3

def makeData(data):
    open, high, low, close = data[1: 5]
    if open < close:
        if open > low and high > close:
            arr = [ open, low, high, close]
        elif open == low and high > close:
            arr = [ open, high, close]
        elif open > low and high == close:
            arr = [ open, low, high]
        else:
            arr = [ open, close]
    elif open > close:
        if close > low and high > open:
            arr = [ open, high, low, close]
        elif close == low and high > open:
            arr = [ open, high, close]
        elif close > low and high == open:
            arr = [ open, close]
        else:
            arr = [ open, close]
    else:
        if (high - open) > (open - low):
            arr = [open, low, high, close]
        elif (high - open) < (open - low):
            arr = [open, high, low, close]
        else: 
            arr = [open, high, low, close]
    prices = []
    for i in range(len(arr)-1):
        add = 5 if arr[i] < arr[i+1] else -5
        for price in range(arr[i], arr[i+1], add):

            prices.append(price)
    #print(open,high,low,close)
    #print(prices)
    return prices


db = sqlite3.connect("data/360750.db")
cu = db.cursor()

cu.execute("select day, open, high, low, close, tr, atr from info_day order by day asc")
data = cu.fetchall()
db.close()

bank = 10000000
banklist = []
buy_atr = None


for i in range(20, len(data)):
    max_high = max( [ j[2] for j in data[i-19: i] ] )
    min_low = min( [ j[3] for j in data[i-9: i] ] )
    before_atr = int(data[i-1][-1])
    before_close = data[i-1][4]

    todayData = makeData(data[i])
    try:
        high, low = todayData[0], todayData[0]
    except Exception as e:
        print(str(e))
        print(todayData)
        import time
        time.sleep(100)
    for price in todayData:
        high = price if price > high else high
        low = price if price < low else low
        tr = max( [ high - low, abs(before_close-high), abs(before_close-low) ] )
        atr = int((before_atr * 19 + tr * 2 ) / 21)
        percent_1 = (bank + sum([ j[0]*j[1] for j in banklist ])) * 0.01
        if len(banklist) > 0: 
            many_sell = sum( [ i[1] for i in banklist ] )
            if price < (banklist[-1][0] - buy_atr * 2):
                bank = bank + many_sell * price
                print("%s S: Price: %5d   Many: %5d  Atr: %5d  Bank: %10d  Sell Cut" % (data[i][0], price, sum([j[1] for j in banklist]), buy_atr, bank))
                banklist = []
                buy_atr = None
            elif price < min_low:
                bank = bank + many_sell * price
                print("%s S: Price: %5d   Many: %5d  Atr: %5d  Bank: %10d  Sell Under 10" % (data[i][0], price, sum([j[1] for j in banklist]), buy_atr, bank))
                banklist = []
                buy_atr = None
            elif price > banklist[-1][0] + buy_atr:
                many = int(percent_1) // atr
                if bank > many * price:
                    bank = bank - price * many
                    banklist.append((price, many))
                    print("%s B: Price: %5d   Many: %5d  Atr: %5d  Bank: %10d  Buy Over ATR" % (data[i][0], price, sum([j[1] for j in banklist]), buy_atr, bank+sum([ j[0]*j[1] for j in banklist])))
        else:
            many = int(percent_1) // atr
            if price > max_high: 
                buy_atr = atr
                bank = bank - price * many
                banklist.append((price, many))
                print("%s B: Price: %5d   Many: %5d  Atr: %5d  Bank: %10d " % (data[i][0], price, many, buy_atr, bank+price*many))
    #print(data[i])     