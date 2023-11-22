from pymongo import MongoClient
from collections import defaultdict


def crawl_borrow_event_all(chain="ethereum"):
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_borrow = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "BORROW"}
    borrow_objects = _event_borrow.find(filter_criteria)
    borrow_objects = list(borrow_objects)
    # TODO: Tra lai data


def crawl_borrow_event(wallet_addresses, chain="ethereum", detail=True):
    """
    input: list address of wallets, name of chain
    output: dict {key: address of wallet, value: total of borrow}
    """
    # output
    total_borrow = defaultdict(dict)
    borrow_events = defaultdict(lambda: defaultdict(dict))

    # Get event
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_borrow = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "BORROW", "wallet": {"$in": wallet_addresses}}
    borrow_objects = _event_borrow.find(filter_criteria)
    borrow_objects = list(borrow_objects)

    token_price_dict = {}
    for tmp in borrow_objects:
        token_adress = tmp.get("reserve")
        amount = tmp.get("amount")
        if token_price_dict.get(token_adress) is None and token_adress is not None:
            token_price_dict[token_adress] = 0.0
    # Get price
    connection_url = "mongodb://klgReaderHoan:klg_reader_hoan_123@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017"
    connection = MongoClient(connection_url)
    ethereum_blockchain_lending = connection["knowledge_graph"]
    _smart_contracts = ethereum_blockchain_lending["smart_contracts"]
    for key in token_price_dict.keys():
        filter_smartcontract = {"_id": f"0x1_{key}"}
        smart_contracts_object = _smart_contracts.find_one(filter_smartcontract)
        token_price_dict[key] = smart_contracts_object.get("price")

    # Get borrow tai aave, compound
    # Processing
    for tmp in borrow_objects:
        wallet_address = tmp.get("wallet")
        token_adress = tmp.get("reserve")
        amount = tmp.get("amount")
        contract_address = tmp.get("contract_address")
        if token_adress is not None:
            if detail:
                if (
                    borrow_events[wallet_address][contract_address].get(token_adress)
                    is not None
                ):
                    borrow_events[wallet_address][contract_address][token_adress] += (
                        amount * token_price_dict[token_adress]
                    )
                else:
                    borrow_events[wallet_address][contract_address][token_adress] = (
                        amount * token_price_dict[token_adress]
                    )
            else:
                if borrow_events[wallet_address].get(contract_address) is not None:
                    total_borrow[wallet_address][contract_address] += (
                        amount * token_price_dict[token_adress]
                    )
                else:
                    total_borrow[wallet_address][contract_address] = (
                        amount * token_price_dict[token_adress]
                    )
    if detail:
        return borrow_events
    else:
        return total_borrow


def crawl_borrow_total(wallet_addresses, chain="ethereum"):
    """
    input: list address of wallets, name of chain
    output: dict {key: address of wallet, value: total of borrow}
    """
    # output
    total_borrow = defaultdict(float)
    borrow_events = defaultdict(lambda: defaultdict(dict))

    # Get event
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_borrow = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "BORROW", "wallet": {"$in": wallet_addresses}}
    borrow_objects = _event_borrow.find(filter_criteria)
    borrow_objects = list(borrow_objects)

    token_price_dict = {}
    for tmp in borrow_objects:
        token_adress = tmp.get("reserve")
        amount = tmp.get("amount")
        if token_price_dict.get(token_adress) is None and token_adress is not None:
            token_price_dict[token_adress] = 0.0
    # Get price
    connection_url = "mongodb://klgReaderHoan:klg_reader_hoan_123@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017"
    connection = MongoClient(connection_url)
    ethereum_blockchain_lending = connection["knowledge_graph"]
    _smart_contracts = ethereum_blockchain_lending["smart_contracts"]
    for key in token_price_dict.keys():
        filter_smartcontract = {"_id": f"0x1_{key}"}
        smart_contracts_object = _smart_contracts.find_one(filter_smartcontract)
        token_price_dict[key] = smart_contracts_object.get("price")

    # Get borrow tai aave, compound
    # Processing
    for tmp in borrow_objects:
        wallet_address = tmp.get("wallet")
        token_adress = tmp.get("reserve")
        amount = tmp.get("amount")
        contract_address = tmp.get("contract_address")
        if token_adress is not None:
            total_borrow[wallet_address] += amount * token_price_dict[token_adress]
    return total_borrow
