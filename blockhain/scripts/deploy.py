#!/usr/bin/python3

from brownie import Cubo, CuboDaoV1, Dai, accounts


def main():
    dai = Dai.deploy({'from': accounts[0]})
    cubo = Cubo.deploy({'from': accounts[0]})
    dao = CuboDaoV1.deploy(cubo, dai,{'from': accounts[0]})
    print(dao)
    cubo.setDaoContract(dao, {'from': accounts[0]})
    return
