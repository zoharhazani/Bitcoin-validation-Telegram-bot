import json
import requests
import urllib
from someBitcoin import someBitcoin

class bitcoinValidationBot:

    # the TOKEN , URL , USERNAME_BOT i got from the botFather And they know how to link
    # the app I wrote to the Telegram page itself

    TOKEN = "5439715785:AAE6S0qNo6LBG_Nwh7pd-OV8yIcvZOUDCVs"
    URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    USERNAME_BOT = "zoharh_bot"

    # With the help of tempBIT I can build a Bitcoin type object that will help me
    # check if the address is correct and get the appropriate balance
    tempBIT = someBitcoin()

    # ctor
    def __init__(self):
        print("build")

    # Tostring
    def __str__(self) -> str:
        return f'<the TOKEN is: {self.TOKEN}, the URL is : {self.URL}, the USERNAME_BOT is : {self.USERNAME_BOT}>'

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def echo_all(self, updates):
        for update in updates["result"]:
            if update.get("message") is not None:
                if update.get("message", {}).get("text") is not None:
                    text = update["message"]["text"]
                    split_data = text.split("\n")
                    chat = update["message"]["chat"]["id"]
                    # check if we want to test our bot
                    if text == "/test" or text == "/test@" + self.USERNAME_BOT:
                        text = "test response"
                        self.send_message(text, chat)
                    # check if we want to start our bot
                    elif text == "hi" or text == "/start" or text == "/start@" + self.USERNAME_BOT:
                        self.send_message("Welcome to the bot of Lahav 433 unit! Please enter a valid Bitcoin "
                                          "address, its may take a couple of sec to get the result :) ", chat)
                    # check if the address is correct.
                    else:
                        if len(split_data) > 20:
                            self.send_message("There are more than 20 lines, The bot will validate the first 20.", chat)
                            split_data = split_data[0:20]
                        for res in split_data:
                            self.tempBIT.address = res
                            if self.tempBIT.validate_bitcoin_address(res):
                                self.send_message(
                                    f"The address: {res}\n is a valid Bitcoin address.\nThe balance of the account is :{self.tempBIT.get_balance(res)}",
                                    chat)
                            elif not self.tempBIT.validate_bitcoin_address(res):
                                self.send_message(f"{res} is not a valid address.", chat)

    def send_message(self, text, chat_id):
        tot = urllib.parse.quote_plus(text)
        url = self.URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
        self.get_url(url)


"""
    def send_document(self,doc, chat_id):
        files = {'document': open(doc, 'rb')}
        requests.post(self.URL + "sendDocument?chat_id={}".format(chat_id), files=files)

    def send_image(self,doc, chat_id):
        files = {'photo': open(doc, 'rb')}
        requests.post(self.URL + "sendPhoto?chat_id={}".format(chat_id), files=files)
"""


# ************************************ MAIN **********************************************************
def main():
    # create the bot
    bot = bitcoinValidationBot()
    last_update_id = None
    while True:
        updates = bot.get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = bot.get_last_update_id(updates) + 1
                bot.echo_all(updates)


if __name__ == '__main__':
    main()
