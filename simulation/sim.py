from time import sleep
from random import randint
from datetime import datetime
import threading, requests, argparse


arg_parser = argparse.ArgumentParser(prog="Warmify simulator")
arg_parser.add_argument("token")
args = arg_parser.parse_args()

TOKEN = args.token
API_URL = "http://localhost:8000/api"
#TEN_MINUTES = 600
TEN_MINUTES = 1
#ONE_HOUR = 3600
#FOUR_HOURS = 36000
ONE_HOUR = 2
FOUR_HOURS = 4

heater_is_on = False

def usage_thread():
    while True:
        sleep_time = randint(TEN_MINUTES, FOUR_HOURS)
        sleep(sleep_time)
        current_datetime = datetime.now()
        print("Usage event detected at {}".format(current_datetime.strftime("%d/%m/%y, %H:%M:%S")))
        send_usage()

def schedule_thread():
    global heater_is_on
    while True:
        status = get_status()
        if status != heater_is_on:
            heater_is_on = not heater_is_on
            print("Turning heater {}.".format("on" if status else "off"))
        else:
            print("Heater status: {}".format("on" if status else "off"))
        sleep(ONE_HOUR)

def send_usage():
    timestamp = datetime.now()
    data = {"timestamp": timestamp.isoformat(), "token": TOKEN}
    r = requests.post("{}/log/".format(API_URL), json=data)
    if r.status_code == 201:
        print("event sent.")

def get_status():
    headers = {"Authorization": TOKEN}
    r = requests.get("{}/status/".format(API_URL), headers=headers)
    json_data = r.json()
    return json_data.get("status")

def main():
    t1 = threading.Thread(target=usage_thread)
    t2 = threading.Thread(target=schedule_thread)
    
    t1.start()
    t2.start()

    #t1.join()
    #t2.join()

if __name__ == "__main__":
    main()
