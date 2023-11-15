from pymongo import MongoClient
from collections import defaultdict
import json


def crawl_deposit_event_all(chain="ethereum"):
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_deposit = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "DEPOSIT"}
    deposit_objects = _event_deposit.find(filter_criteria)

    deposit_dict = defaultdict(
        int
    )  # Key: wallet address, value: numbers of liquidation
    for obj in deposit_objects:
        wallet_adress = obj.get("wallet")
        if deposit_dict.get(wallet_adress) is None:
            deposit_dict[wallet_adress] = 1
        else:
            deposit_dict[wallet_adress] += 1
    with open(
        f"D:/Project/Data-Analysis/New_DataAnalysis/data/deposit/{chain}_wallet_deposit.json",
        "w",
    ) as f:
        json.dump(deposit_dict, f, indent=4)


