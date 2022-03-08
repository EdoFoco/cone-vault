#!/usr/bin/python3
from test_utils import transfer_funds

def test_withdraw(accounts, cuboToken, daiToken, coneVaultContract, daoContract):
    #arrange
    amount1 = 20 * 10**18
    amount2 = 20 * 10**18

    ## send tokens from admin to user
    transfer_funds(accounts[0], accounts[1], amount1, cuboToken)
    transfer_funds(accounts[0], accounts[1], amount1, daiToken)
    transfer_funds(accounts[0], accounts[2], amount2, cuboToken)
    transfer_funds(accounts[0], accounts[2], amount2, daiToken)

    init_mgmt_cubo_balance = 100*10**18
    init_mgmt_dai_balance = daiToken.balanceOf(accounts[9], {'from': accounts[9]})

    ## approve contract
    cuboToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
    daiToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
    cuboToken.approve(coneVaultContract, amount2, {'from': accounts[2]})
    daiToken.approve(coneVaultContract, amount2, {'from': accounts[2]})

    coneVaultContract.deposit(amount1, amount1, {'from': accounts[1]})
    coneVaultContract.deposit(amount2, amount2, {'from': accounts[2]})
    cubo_balance = cuboToken.balanceOf(accounts[1], {'from': accounts[1]})
    dai_balance = daiToken.balanceOf(accounts[1], {'from': accounts[1]})   

    print(cubo_balance)
    print(dai_balance)

    # act
    withdraw_amount = 10 * 10**18
    coneVaultContract.withdraw(withdraw_amount, withdraw_amount, {'from': accounts[1]})

    # assert
    mgmt_cubo_balance = cuboToken.balanceOf(accounts[9], {'from': accounts[9]})
    mgmt_dai_balance = daiToken.balanceOf(accounts[9], {'from': accounts[9]})

    cubo_balance = cuboToken.balanceOf(accounts[1], {'from': accounts[1]})
    dai_balance = daiToken.balanceOf(accounts[1], {'from': accounts[1]})

    diff_mgmt_cubo = mgmt_cubo_balance - init_mgmt_cubo_balance
    diff_mgmt_dai = mgmt_dai_balance - init_mgmt_dai_balance

    invested_amounts = coneVaultContract.getInvestedAmounts({'from': accounts[1]})

    assert cubo_balance == withdraw_amount - diff_mgmt_cubo
    assert dai_balance == withdraw_amount - diff_mgmt_dai
    assert invested_amounts[0] == amount1 - withdraw_amount
    assert invested_amounts[1] == amount1 - withdraw_amount
