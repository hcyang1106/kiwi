import time
import yaml
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

updater = Updater("5251317898:AAGfF6Z_sR45lH8mcSdd2WeyBU34Ncri2m4",
                  use_context=True)


def clockin(update: Update, context: CallbackContext):
    update.message.reply_text("已請求Howger幫打上班卡")

    try:
        with open("users.yaml", 'r') as stream:
            users = yaml.safe_load(stream)
            for user in users:
                print(user)
                if user["username"] == update.message.from_user.username:
                    id = user["id"]
                    password = user["password"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()

        driver.get("https://cloud.nueip.com/login/83663709")

        elem = driver.find_element(By.ID, "username_input")
        elem.send_keys(id)

        elem = driver.find_element(By.ID, "password-input")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)

        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": "https://cloud.nueip.com/home",
                "permissions": ["geolocation"]
            },
        )
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride",
                               {
                                   "latitude": 25.02283095064086,
                                   "longitude": 121.54949954857622,
                                   "accuracy": 99.9999,
                               }, )
        js = 'document.getElementById("clockin").click();'
        driver.execute_script(js)
    except:
        update.message.reply_text("打卡失敗")
        return
    else:
        update.message.reply_text("打卡成功")
        driver.close()


def clockout(update: Update, context: CallbackContext):
    update.message.reply_text("已請求Howger幫打下班卡")

    try:
        with open("users.yaml", 'r') as stream:
            users = yaml.safe_load(stream)
            for user in users:
                print(user)
                if user["username"] == update.message.from_user.username:
                    id = user["id"]
                    password = user["password"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()

        driver.get("https://cloud.nueip.com/login/83663709")

        elem = driver.find_element(By.ID, "username_input")
        elem.send_keys(id)

        elem = driver.find_element(By.ID, "password-input")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)

        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": "https://cloud.nueip.com/home",
                "permissions": ["geolocation"]
            },
        )
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride",
                               {
                                   "latitude": 25.02283095064086,
                                   "longitude": 121.54949954857622,
                                   "accuracy": 99.9999,
                               }, )
        js = 'document.getElementById("clockout").click();'
        driver.execute_script(js)
    except:
        update.message.reply_text("打卡失敗")
        return
    else:
        update.message.reply_text("打卡成功")
        driver.close()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /clockin - 打上班卡
    /clockout - 打下班卡""")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('clockout', clockout))
updater.dispatcher.add_handler(CommandHandler('clockin', clockin))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
