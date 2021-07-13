import telebot
import yfinance as yf

# stored the api key in var file and imported that here.
API_KEY = API_KEY
bot = telebot.TeleBot(API_KEY)

# runs by sending '/greet' in the bot chat
@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message, "Hey Wassup ? How You doin ?")

# runs by sending '/hello' in the bot chat
@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello There !!!!!!!!")

# runs by sending '/wsb' in the bot chat
@bot.message_handler(commands=['wsb'])
def get_stocks(message):
    response = ""
    stocks = ["gme", "amc", "nok"]
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='2d', interval='1d')
        data = data.reset_index()
        response += f"-----------{stock}---------\n"
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)

        print()

    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"

    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)
        # stock_request(message)

# defining custom commmands without '/'
def stock_request(message):
    request = message.text.split()
    if len(request)<2 or request[0].lower() not in "price":
        return False
    else:
        return True

# runs by passing 'price<space>stockid' to get the stock info of last 5 minutes separated by 1 minute
@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    comapanyName = yf.Ticker(request).info['longName']
    data = yf.download(tickers=request, period='5m', interval='1m')
    if data.size>0:
        data = data.reset_index()
        data['format_date'] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id, f'The {comapanyName} stock price is:\n'+data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id, "No Data!!!!!!!!!!!")
    pass




bot.polling()
