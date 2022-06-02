#!/usr/bin/python3
from test_utils import transfer_funds

def test_deposit_and_get_balances(accounts, cuboToken, daiToken, coneVaultContract):
   #arrange
   amount = 100 * 10**18
   
   ## send tokens from admin to user
   cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
   daiToken.approve(accounts[1], amount, {'from': accounts[0]})
   cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})
   daiToken.transfer(accounts[1], amount, {'from': accounts[0]})

   dai_balance = daiToken.balanceOf(accounts[1])
   cubo_balance = cuboToken.balanceOf(accounts[1])

   ## approve contract
   cuboToken.approve(coneVaultContract, dai_balance, {'from': accounts[1]})
   daiToken.approve(coneVaultContract, cubo_balance, {'from': accounts[1]})

   # act
   coneVaultContract.deposit(cubo_balance, dai_balance,{'from': accounts[1]})

   # assert
   investorDetails = coneVaultContract.getInvestedAmounts({'from': accounts[1]})

   assert investorDetails[0] == cubo_balance
   assert investorDetails[1] == dai_balance


def test_deposit_with_more_users(accounts, cuboToken, daiToken, coneVaultContract):
   #arrange
   amount1 = 70 * 10**18
   amount2 = 20 * 10**18

   ## send tokens from admin to user
   transfer_funds(accounts[0], accounts[1], amount1, cuboToken)
   transfer_funds(accounts[0], accounts[1], amount1, daiToken)
   transfer_funds(accounts[0], accounts[2], amount2, cuboToken)
   transfer_funds(accounts[0], accounts[2], amount2, daiToken)

   ## approve contract
   cuboToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   daiToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   cuboToken.approve(coneVaultContract, amount2, {'from': accounts[2]})
   daiToken.approve(coneVaultContract, amount2, {'from': accounts[2]})

   # act
   coneVaultContract.deposit(amount1, amount1, {'from': accounts[1]})
   coneVaultContract.deposit(amount2, amount2, {'from': accounts[2]})

   # assert
   cuboNodes = coneVaultContract.getNodes({'from': accounts[1]})
   investor1Details = coneVaultContract.getInvestedAmounts({'from': accounts[1]})
   investor2Details = coneVaultContract.getInvestedAmounts({'from': accounts[2]})
   
   assert cuboNodes[0] == 0
   assert investor1Details[0] == amount1
   assert investor1Details[1] == amount1
   assert investor2Details[0] == amount2
   assert investor2Details[1] == amount2


def test_deposit_with_more_users_and_node_and_avoid_overcharge(accounts, cuboToken, daiToken, coneVaultContract):
   #arrange
   amount1 = 80 * 10**18
   amount2 = 30 * 10**18

   ## send tokens from admin to user
   transfer_funds(accounts[0], accounts[1], amount1, cuboToken)
   transfer_funds(accounts[0], accounts[1], amount1, daiToken)
   transfer_funds(accounts[0], accounts[2], amount2, cuboToken)
   transfer_funds(accounts[0], accounts[2], amount2, daiToken)

   ## approve contract
   cuboToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   daiToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   cuboToken.approve(coneVaultContract, amount2, {'from': accounts[2]})
   daiToken.approve(coneVaultContract, amount2, {'from': accounts[2]})

   # act
   coneVaultContract.deposit(amount1, amount1, {'from': accounts[1]})
   coneVaultContract.deposit(amount2, amount2, {'from': accounts[2]})

   # assert
   cuboNodes = coneVaultContract.getNodes({'from': accounts[1]})
   investor1Details = coneVaultContract.getInvestedAmounts({'from': accounts[1]})
   investor2Details = coneVaultContract.getInvestedAmounts({'from': accounts[2]})
   final_amount2 = amount2 - (10 * 10 ** 18)
   print(final_amount2)

   assert cuboNodes[0] == 1
   assert investor1Details[0] == amount1
   assert investor1Details[1] == amount1
   assert investor2Details[0] == final_amount2
   assert investor2Details[1] == final_amount2

