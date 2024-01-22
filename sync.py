import gkeepapi
import requests
import os
import uuid
import json
import schedule
import time

def getMatlistanToken():
    response = requests.post("https://api2.matlistan.se/Sessions", json={
        "email": os.environ.get("MATLISTAN_EMAIL"),
        "password": os.environ.get("MATLISTAN_PASSWORD"),
        "deviceId": str(uuid.uuid4())
    })
    response.raise_for_status()

    json = response.json()
    return json["bearerToken"]

def addItemToMatlistan(item, bearerToken):
    response = requests.post("https://api2.matlistan.se/Items", json={
        "text": item,
        "listId": os.environ.get("MATLISTAN_LIST_ID")
    }, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearerToken}",
        "X-Clientid": "alacart0"
    })
    response.raise_for_status()

def storeState(keep):
    state = keep.dump()
    fh = open('/data/state', 'w')
    json.dump(state, fh)

def loadState():
    if not os.path.exists("/data/state"):
        return None

    fh = open('/data/state', 'r')
    return json.load(fh)

def storeKeepToken(token):
    fh = open('/data/token', 'w')
    fh.write(token)

def getKeepToken():
    if not os.path.exists("/data/token"):
        return None

    fh = open('/data/token', 'r')
    return fh.read()

def keepLogin():
    global loggedIn
    global keep

    if loggedIn:
        print("already logged in")
        return keep

    print("logging in to Google Keep")
    keep = gkeepapi.Keep()
    token = getKeepToken()
    state = loadState()

    if token:
        try:
            print("logging in with token")
            keep.resume(os.environ.get("GOOGLE_EMAIL"), token, state=state)
            loggedIn = True
        except gkeepapi.exception.LoginException:
            print("Token expired")
            token = None

    if not loggedIn:
        print("logging in with password")
        keep.login(os.environ.get("GOOGLE_EMAIL"), os.environ.get("GOOGLE_PASSWORD"), state=state)
        loggedIn = True

    if not loggedIn:
        print("login failed")
        exit()

    token = keep.getMasterToken()
    storeKeepToken(token)
    return keep

def sync():
    keep.sync()
    note_list = keep.get(os.environ.get("KEEP_LIST_ID"))
    list_items = note_list.unchecked

    if len(list_items) == 0:
        storeState(keep)
        ping_success_webhook()
        print("No new items to sync")
        return


    try:
        matlistan_token = getMatlistanToken()

        for item in list_items:
            print("syncing to Matlistan:", item.text)
            addItemToMatlistan(item.text, matlistan_token)
            item.checked = True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        keep.sync()
        storeState(keep)
        ping_success_webhook()

def ping_success_webhook():
    if os.environ.get("SUCCESS_WEBHOOK_URL"):
        requests.get(os.environ.get("SUCCESS_WEBHOOK_URL"))


print("Booting up")
loggedIn = False
keep = keepLogin()

print ("Starting on-off sync")
sync()

interval = int(os.environ.get("SYNC_INTERVAL", 45))
print("Starting continuous sync every", interval, "minutes")

schedule.every(45).minutes.do(sync)
while True:
    schedule.run_pending()
    time.sleep(10)
