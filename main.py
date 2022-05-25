#!/usr/bin/env python3

import configparser
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

# Configuration (config.ini) parse
# TODO: Add condition to check if file and the required data exist
config = configparser.ConfigParser()
config.read("config.ini")

BOT_TOKEN = config["bot"]["token"]

# Initialize requests session
session = requests.Session()

# Hax & Woiden "Create VPS" page URL
haxCreateVPSPage = "https://hax.co.id/create-vps/"
woidenCreateVPSPage = "https://woiden.id/create-vps/"

# Function: Parse page
def getAvailableServer(update, context, site):
    if site == "Hax":
        requestPage = session.get(haxCreateVPSPage).content
    elif site == "Woiden":
        requestPage = session.get(woidenCreateVPSPage).content
    else:
        print("Unknown site parsed as argument!")
        exit(1)
    parsedCreateVPSPage = BeautifulSoup(requestPage, "html.parser")
    availableServers = parsedCreateVPSPage.find("select", {"id": "datacenter"}).find_all("option")[1:] # Skip the first entry ("--select--")
    totalAvailableServers = len(availableServers)

    if totalAvailableServers > 1:
        text = f"There is/are <b>{totalAvailableServers}</b> available servers at {site}:\n\n"
        for availableServer in availableServers:
            text += f"• {availableServer.text}\n"
    else:
        text = f"Sorry, there are <b>no</b> available servers at {site}!"

    update.message.reply_text(text, parse_mode="HTML")

# These two functions below act as getAvailableServer() caller
# Since CommandHandler() can't accept function arguments
# TODO: Use better approach
def haxSendInfo(update, context):
    getAvailableServer(update, context, "Hax")
def woidenSendInfo(update, context):
    getAvailableServer(update, context, "Woiden")

if __name__ == "__main__":
    # Telegram Bot initialization
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("hax", haxSendInfo, run_async=True))
    dispatcher.add_handler(CommandHandler("woiden", woidenSendInfo, run_async=True))

    print("Bot initialized!")
    updater.start_polling()
