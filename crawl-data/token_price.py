from collections import defaultdict
from pymongo import MongoClient


def get_token_price_dict(token_addresses):
    token_price_dict = defaultdict(float)
    # Get price
    connection_url = "mongodb://klgReaderHoan:klg_reader_hoan_123@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017"
    connection = MongoClient(connection_url)
    ethereum_blockchain_lending = connection["knowledge_graph"]
    _smart_contracts = ethereum_blockchain_lending["smart_contracts"]
    for address in token_addresses:
        filter_smartcontract = {"_id": f"0x1_{address}"}
        smart_contracts_object = _smart_contracts.find_one(filter_smartcontract)
        token_price_dict[address] = smart_contracts_object.get("price")
    return token_price_dict