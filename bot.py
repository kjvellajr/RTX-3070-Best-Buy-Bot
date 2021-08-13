import asyncio
import datetime
import os
import time
from slack_sdk.webhook.async_client import AsyncWebhookClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info

# setup slack url
SLACK_URL = os.getenv("SLACK_URL")
if SLACK_URL is None:
    print("Missing environment variable SLACK_URL. Example setup:")
    print('$ export SLACK_URL="https://hooks.slack.com/services/foo/bar/baz"')
    print("Exiting")
    exit()

# make sure this path is correct
PATH = os.path.dirname(os.path.realpath(__file__)) + "/opt/chromedriver"

driver = webdriver.Chrome(PATH)

# urls of bestbuy items
RTX3080_EVGA = "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400"
RTX3070LINK1 = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
RTX3070LINK2 = "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6437912.p?skuId=6437912"
XBOXONETEST = "https://www.bestbuy.com/site/microsoft-xbox-one-s-1tb-console-bundle-white/6415222.p?skuId=6415222"
GAMING_CHAIR = "https://www.bestbuy.com/site/akracing-core-series-sx-gaming-chair-black/6215628.p?skuId=6215628"

# set the item to scan for
BOT_URL = RTX3080_EVGA

# method to send a slack message
async def send_message_via_webhook(msg: str, url: str):
    webhook = AsyncWebhookClient(SLACK_URL)
    response = await webhook.send(text="{} {}".format(msg, url))
    assert response.status_code == 200
    assert response.body == "ok"

driver.get(BOT_URL)

asyncio.run(send_message_via_webhook("Bot started for", BOT_URL))

# main loop
while True:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        print("{} Retry in 50 sec".format(datetime.datetime.now()))
        time.sleep(50)
        driver.refresh()
        continue

    print("{} Found! Sending slack message.".format(datetime.datetime.now()))
    asyncio.run(send_message_via_webhook("Availability found!", BOT_URL))
    time.sleep(50)

