# #!/usr/bin/python3
# import brownie


# def test_mint_node(accounts, daoContract, daiToken, cuboToken):

#     # arrange
#     initial_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})

#     amount = 100 * 10**18
    
#     cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
#     daiToken.approve(accounts[1], amount, {'from': accounts[0]})

#     cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})
#     daiToken.transfer(accounts[1], amount, {'from': accounts[0]})

#     dai_balance = daiToken.balanceOf(accounts[1])
#     init_cubo_balance = cuboToken.balanceOf(accounts[1])

#     cuboToken.approve(daoContract, dai_balance, {'from': accounts[1]})
#     daiToken.approve(daoContract, init_cubo_balance, {'from': accounts[1]})
    
#     daoContract.mintNode(accounts[1], init_cubo_balance, dai_balance, 0, {'from': accounts[1]})
#     current_cubo_balance = cuboToken.balanceOf(accounts[1])

#     final_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})
#     daoContract.payInterest(initial_nodes_count, final_nodes_count, {'from': accounts[0]})
    
#     # act
#     daoContract.widthrawInterest(accounts[1], {'from': accounts[1]})
    
#     # assert
#     final_cubo_balance = cuboToken.balanceOf(accounts[1])
#     assert final_cubo_balance > current_cubo_balance
