'''
Chia danh sách ví whale thành ví có borrow và ví không borrow

'''
from pymongo import MongoClient
import json

with open('D:/Project/Data-Analysis/New_DataAnalysis/data/whale/whales.json', 'r') as f:
        whale_dict = json.load(f)
connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"        
# Read ví whale # TODO: Đọc từ DB
def get_wallet(chain = 'ethereum'):    
    
    # Kiem tra tren tat ca mang (protocols)
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _lending_events = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "BORROW"}
    borrow_objects = _lending_events.find(filter_criteria)
    borrow_objects = list(borrow_objects)
    print(1)
    # Get Wallet
    whale_wallet_addresses = []
    for tmp in whale_dict:
        whale_wallet_addresses.append(tmp.get("address"))
    all_borrow_wallets = []
    for tmp in borrow_objects:
        all_borrow_wallets.append(tmp.get("wallet"))
    all_borrow_wallets  = tuple(all_borrow_wallets)
     
    intersection_result = tuple(set(all_borrow_wallets).intersection(whale_wallet_addresses)) # Giao của whale và các ví borrow => ví whale tham gia borrow
    difference_result = tuple(set(whale_wallet_addresses) - set(intersection_result)) # Ví whale không tham gia borrow
    
    with open(
        "D:/Project/Data-Analysis/New_DataAnalysis/data/whale/whale_not_borrow.json", "w"
    ) as f:
        json.dump(list(difference_result), f, indent=4)
    with open(
        "D:/Project/Data-Analysis/New_DataAnalysis/data/whale/whale_borrow.json", "w"
    ) as f:
        json.dump(list(intersection_result), f, indent=4)