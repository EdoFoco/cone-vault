#!/usr/bin/python3
from test_utils import transfer_funds

def test_getInterests_with_more_users(accounts, cuboToken, daiToken, coneVaultContract, daoContract):
   #arrange
   amount1 = 80 * 10**18
   amount2 = 20 * 10**18

   ## send tokens from admin to user
   transfer_funds(accounts[0], accounts[1], amount1, cuboToken)
   transfer_funds(accounts[0], accounts[1], amount1, daiToken)
   transfer_funds(accounts[0], accounts[2], amount2, cuboToken)
   transfer_funds(accounts[0], accounts[2], amount2, daiToken)

   init_mgmt_balance = cuboToken.balanceOf(accounts[0], {'from': accounts[0]})
   initial_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})
   
   ## approve contract
   cuboToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   daiToken.approve(coneVaultContract, amount1, {'from': accounts[1]})
   cuboToken.approve(coneVaultContract, amount2, {'from': accounts[2]})
   daiToken.approve(coneVaultContract, amount2, {'from': accounts[2]})

   coneVaultContract.deposit(amount1, amount1, {'from': accounts[1]})
   coneVaultContract.deposit(amount2, amount2, {'from': accounts[2]})
   final_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})
   daoContract.payInterest(initial_nodes_count, final_nodes_count, {'from': accounts[0]})

   # act
   txn = coneVaultContract.claimInterests({'from': accounts[2]})
   print(txn.info())

   # assert
   mgmt_balance = cuboToken.balanceOf(accounts[0], {'from': accounts[0]})
   interests1 = cuboToken.balanceOf(accounts[1], {'from': accounts[1]})
   interests2 = cuboToken.balanceOf(accounts[2], {'from': accounts[2]})
   claimed1 = coneVaultContract.getClaimedRewards(accounts[1], {'from': accounts[2]})
   claimed2 = coneVaultContract.getClaimedRewards(accounts[2], {'from': accounts[2]})
   
   total_interest = interests1 + interests2
   total_amount = amount1 + amount2

   assert interests1 == claimed1
   assert interests2 == claimed2
   assert amount1 / total_amount * 100 == interests1 / total_interest * 100
   assert amount2 / total_amount * 100 == interests2 / total_interest * 100
   assert mgmt_balance > init_mgmt_balance

   
