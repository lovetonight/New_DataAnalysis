from pymongo import MongoClient
import json

# DB

# KLG
connection_url = "mongodb://klgReaderHoan:klg_reader_hoan_123@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017"
connection = MongoClient(connection_url)
blockchain_etl = connection["knowledge_graph"]
wallets = blockchain_etl["wallets"]

# Write

localhost = MongoClient("mongodb://localhost:27017/")
mydb = localhost["data-analysis"]
mycol = mydb["label"]

def get_wallets(chain = "ethereum"):
    with open(
        f"D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}_wallet_liquidate.json",
        "r",
    ) as f:
        wallet_liquidate = json.load(f)
    # Process
    
    # Get all wallets
    all_wallets = []
    for key, value in wallet_liquidate.items():
        all_wallets.append(f"0x1_{key}")
        
    # Liqudate > 3 times
    list_wallets_3times_liquidate = []
    for key, value in wallet_liquidate.items():
        if value > 3:
            list_wallets_3times_liquidate.append(f"0x1_{key}")
    # Liquidate <= 3 times
    list_wallets_liquidate = list(set(all_wallets)-set(list_wallets_3times_liquidate))
    
    ## Get object
    
    # Liquidate > 3 lần
    filter_criteria_1 = {
        "_id": {"$in": list_wallets_3times_liquidate},
        "borrowInUSD": {"$exists": True},
    }
    liquidate_3times_objects = wallets.find(filter_criteria_1)
    
    # Liquidate <= 3 lần
    filter_criteria_2 = {
    "_id": {"$in": list_wallets_liquidate},
    "borrowInUSD": {"$exists": True},
    }
    
    
    
    label1_addresses = []
    label2_addresses = []
    
    # 
    liquidate_objects = wallets.find(filter_criteria_2)
    for obj in liquidate_3times_objects:
        if obj.get("balanceInUSD") == 0 or obj.get("balanceInUSD") is None:
            label1_addresses.append(obj.get("address"))
        else:
            if obj.get("borrowInUSD") / obj.get("balanceInUSD") > 0.8:
                label1_addresses.append(obj.get("address"))
            else:
                label2_addresses.append(obj.get("address"))
    #         
    liquidate_objects = wallets.find(filter_criteria_2)
    for obj in liquidate_objects:
        if obj.get("balanceInUSD") == 0 or obj.get("balanceInUSD") is None:
            continue
        else:
            label2_addresses.append(obj.get("address"))
    return label1_addresses, label2_addresses


def labeling(chain = "ethereum"):
    object = []
    label1_addresses, label2_addresses = get_wallets(chain)
    for address in label1_addresses:
        chain_id = '0x1'
        obj = {}
        obj["address"] = address
        obj["label"] = 1
        obj["chain"] = chain
        obj["id"] = f'{chain_id}_{address}'
        object.append(obj)
    for address in label2_addresses:
        chain_id = '0x1'
        obj = {}
        obj["address"] = address
        obj["label"] = 2
        obj["chain"] = chain
        obj["id"] = f'{chain_id}_{address}'
        object.append(obj)
    for obj in object:
        query = {"_id": obj["id"]}
        update_data = {"$set": obj}
        mycol.update_one(query, update_data, upsert=True)

    
   
