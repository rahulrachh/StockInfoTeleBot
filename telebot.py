import var
import telebot
import yfinance as yf

# created a var.py file where I stored the apikey and importing that from var.py file
API_KEY = var.api_key
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message, "Hey Wassup ? How You doin ?")

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello There !!!!!!!!")

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

    def stock_request(message):
        request = message.text.split()
        if len(request)<2 or request[0].lower() not in "price":
            return False
        else:
            return True


    @bot.message_handler(func=stock_request)
    def send_price(message):
        pass




bot.polling()
