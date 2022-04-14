from unittest.mock import Mock
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS,)

def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # If we are on a persistent network like rinkeby, use the associated address
    #otherwise. deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f"The active network is {network.show_active()}")
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
            ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify"), #simply ["verify"] is also correct but we might run into index error so used .get("verify")
        )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()
