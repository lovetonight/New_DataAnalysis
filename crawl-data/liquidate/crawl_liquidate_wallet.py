from pymongo import MongoClient
from collections import defaultdict
import json
def craw_liquidate_wallet(chain = 'ethereum'):
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_liquidate = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "LIQUIDATE"}
    liquidate_objects = _event_liquidate.find(filter_criteria)
    
    liquidate_dict = defaultdict(int) # Key: wallet address, value: numbers of liquidation
    for obj in liquidate_objects:
        wallet_adress = obj.get("wallet")
        if liquidate_dict.get(wallet_adress) is None:
            liquidate_dict[wallet_adress] = 1
        else:
            liquidate_dict[wallet_adress] +=1
    with open(f'D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}_wallet_liquidate.json','w') as f:
        json.dump(liquidate_dict, f, indent=4)