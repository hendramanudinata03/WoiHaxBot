#!/usr/bin/env python3

import configparser
import requests_cache
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

# Configuration (config.ini) parse
# TODO: Add condition to check if file and the required data exist
config = configparser.ConfigParser()
config.read("config.ini")

BOT_TOKEN = config["bot"]["token"]

# Initialize requests session + cache
session = requests_cache.CachedSession("woihax_cache", expire_after=180)
session.headers.update(
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
)

# Hax & Woiden "Create VPS" page URL
haxCreateVPSPage = "https://hax.co.id/create-vps/"
woidenCreateVPSPage = "https://woiden.id/create-vps/"
createVPSPageDict = {
    "Hax": haxCreateVPSPage,
    "Woiden": woidenCreateVPSPage
}

# Function: Parse page
def getAvailableServer(update, context):
    arrayText = []
    for key, value in createVPSPageDict.items():
        requestPage = session.get(value).content
        parsedCreateVPSPage = BeautifulSoup(requestPage, "html.parser")
        availableServers = parsedCreateVPSPage.find("select", {"id": "datacenter"}).find_all("option")[1:] # Skip the first entry ("--select--")
        totalAvailableServers = len(availableServers)

        text = f"<b>{key}</b>:\n"
        if totalAvailableServers >= 1:
            text += f"There is/are <b>{totalAvailableServers}</b> available servers at {key}:\n\n"
            for availableServer in availableServers:
                text += f"• {availableServer.text}\n"
        else:
            text += f"Sorry, there are <b>no</b> available servers at {key}!"
        arrayText.append(text)

    # Overall resulting text
    # arrayText[0] = Hax
    # arrayText[1] = Woiden
    resultText = f"{arrayText[0]}\n\n{arrayText[1]}"

    # /list <blablabla>
    if len(context.args) == 1:
        if context.args[0] == "Hax" or context.args[0] == "hax":
            update.message.reply_text(arrayText[0], parse_mode="HTML")
        elif context.args[0] == "Woiden" or context.args[0] == "woiden":
            update.message.reply_text(arrayText[1], parse_mode="HTML")
        else:
            update.message.reply_text(resultText, parse_mode="HTML")
    # /list
    else:
        update.message.reply_text(resultText, parse_mode="HTML")

if __name__ == "__main__":
    # Telegram Bot initialization
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    # /list
    dispatcher.add_handler(CommandHandler("list", getAvailableServer, run_async=True))

    print("Bot initialized!")
    updater.start_polling()
