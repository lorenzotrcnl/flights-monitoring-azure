import os
import time
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from FlightRadar24 import FlightRadar24API

from azure.cosmos import CosmosClient

load_dotenv()

COSMOS_CONNECTION_STR = os.getenv("COSMOS_CONNECTION_STR")
FR_API = FlightRadar24API()
RADIUS = 50 * 1000  # 50km
BOUNDS = FR_API.get_bounds_by_point(41.795061, 12.253376, RADIUS)

def fetch_airplane_data():
    flights = []
    for fli in FR_API.get_flights(bounds=BOUNDS):
        dat = vars(fli)
        dat['fr_id'] = dat.pop('id')
        dat['id'] = str(uuid.uuid4())
        dat['ts'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
        flights.append(dat)

    return flights

def sink_data(container, data):
    print('SENDING MESSAGES ------------------> ', len(data), ' current flights')
    for fli in data:
        container.upsert_item(fli)
        time.sleep(0.1)


if __name__ == '__main__':
    print("[INITIALIZING]")
    cosmos_client = CosmosClient.from_connection_string(conn_str=COSMOS_CONNECTION_STR)
    cosmos_database = cosmos_client.get_database_client("flights-cosmos-db")
    cosmos_container = cosmos_database.get_container_client("flights")

    print("[READY]\n")
    try:
        while True:
            airplane_data = fetch_airplane_data()
            sink_data(cosmos_container, airplane_data)
    except KeyboardInterrupt:
        print('[STOPPED]')