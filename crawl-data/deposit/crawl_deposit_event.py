from pymongo import MongoClient
from collections import defaultdict


def crawl_deposit_event_all(chain="ethereum"):
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_deposit = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "DEPOSIT"}
    deposit_objects = _event_deposit.find(filter_criteria)
    deposit_objects = list(deposit_objects)
    # TODO: Tra lai data


def crawl_deposit_event(wallet_addresses, chain="ethereum", detail=True):
    """
    input: list address of wallets, name of chain
    output: dict {key: address of wallet, value: total of deposit}
    """
    # output
    total_deposit = defaultdict(float)
    deposit_events = defaultdict(lambda: defaultdict(dict))

    # Get event
    connection_url = "mongodb://etlReader:etl_reader_tsKNV6KFr2GWqqqZ@34.126.84.83:27017,34.142.204.61:27017,34.142.219.60:27017"
    connection = MongoClient(connection_url)
    blockchain_etl = connection[f"{chain}_blockchain_etl"]
    _event_deposit = blockchain_etl["lending_events"]
    filter_criteria = {"event_type": "DEPOSIT", "wallet": {"$in": wallet_addresses}}
    deposit_objects = _event_deposit.find(filter_criteria)
    deposit_objects = list(deposit_objects)

    token_price_dict = {}
    for tmp in deposit_objects:
        if tmp.get("reserve") is None:
            token_adress = tmp.get("contract_address")
        else:
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
        if smart_contracts_object.get("price") is None:
            print(key)
        token_price_dict[key] = smart_contracts_object.get("price")

    # Get deposit tai aave, compound
    # Processing
    for tmp in deposit_objects:
        wallet_address = tmp.get("wallet")
        if tmp.get("reserve") is None:
            token_adress = tmp.get("contract_address")
        else:
            token_adress = tmp.get("reserve")
        amount = tmp.get("amount")
        contract_address = tmp.get("contract_address")
        if  token_price_dict[token_adress] is not None:
            if detail:
                if (
                    deposit_events[wallet_address][contract_address].get(token_adress)
                    is not None
                ):
                    deposit_events[wallet_address][contract_address][token_adress] += (
                        amount * token_price_dict[token_adress]
                    )
                else:
                    deposit_events[wallet_address][contract_address][token_adress] = (
                        amount * token_price_dict[token_adress]
                    )
            else:
                total_deposit[wallet_address] += amount * token_price_dict[token_adress]

    if detail:
        return deposit_events
    else:
        return total_deposit

