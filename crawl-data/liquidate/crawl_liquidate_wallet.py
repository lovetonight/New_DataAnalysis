from pymongo import MongoClient
from collections import defaultdict
import json

myclient = MongoClient("mongodb://localhost:27017/")
data_db = myclient["data-analysis"]
wallet_collection = data_db["wallet"]


def craw_liquidate_wallet(chain="ethereum"):
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_liquidate = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "LIQUIDATE"}
    liquidate_objects = _event_liquidate.find(filter_criteria)

    liquidate_dict = defaultdict(
        int
    )  # Key: wallet address, value: numbers of liquidation
    for obj in liquidate_objects:
        wallet_adress = obj.get("wallet")
        if liquidate_dict.get(wallet_adress) is None:
            liquidate_dict[wallet_adress] = 1
        else:
            liquidate_dict[wallet_adress] += 1
    with open(
        f"D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}_wallet_liquidate.json",
        "w",
    ) as f:
        json.dump(liquidate_dict, f, indent=4)


def get_3_liquidate(chain="ethereum"):
    # Wallet
    with open(
        f"D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}_wallet_liquidate.json",
        "r",
    ) as f:
        wallet_liquidate = json.load(f)

    # DB
    connection_url = "mongodb://klgReaderHoan:klg_reader_hoan_123@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection["knowledge_graph"]
    wallets = blockchain_etl["wallets"]

    # Process
    list_wallets = []
    for key, value in wallet_liquidate.items():
        if value > 3:
            list_wallets.append(f"0x1_{key}")

    #
    all_wallets = []
    for key, value in wallet_liquidate.items():
        all_wallets.append(f"0x1_{key}")

    # Get balance

    filter_criteria = {"_id": {"$in": list_wallets}, "balanceInUSD": {"$lt": 1000}}
    liquidate_objects = wallets.find(filter_criteria)
    addresses = []
    for obj in liquidate_objects:
        addresses.append(obj.get("address"))

    #
    exist_wallet = []
    objects = wallets.find({"_id": {"$in": all_wallets}})
    for obj in objects:
        exist_wallet.append(obj.get("address"))
    # Ghi vao file
    wallet_objects = []
    for address in addresses:
        tmp = {}
        tmp["_id"] = f'0x1_{address}'
        tmp["type"] = "LIQUIDATE"
        tmp["chain"] = chain
        tmp["address"] = address
        # wallet_objects.append(tmp)
        wallet_collection.insert_one(tmp)
    

    # with open(
    #     f"D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}/wallet_low_score.json",
    #     "w",
    # ) as f:
    #     json.dump(addresses, f, indent=4)

    # filtered_wallets = list(set(exist_wallet) - set(addresses))
    # with open(
    #     f"D:/Project/Data-Analysis/New_DataAnalysis/data/liquidate/{chain}/wallet_normal_score.json",
    #     "w",
    # ) as f:
    #     json.dump(filtered_wallets, f, indent=4)

    # check wallet khong co trong klg
    """
    for key, value in wallet_liquidate.items():
        list_wallets.append(f"0x1_{key}")
    print(f'so luong vi liquidate: {len(list_wallets)}')
    filter_criteria = {"_id": {"$in": list_wallets}}
    liquidate_objects = wallets.find(filter_criteria)
    print(f'so luong vi co trong db: {liquidate_objects.count()}')
    """


get_3_liquidate()
