# #!/usr/bin/python3
# import brownie


# def test_mint_node(accounts, daoContract, daiToken, cuboToken):

#     initial_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})

#     amount = 100 * 10**18
    
#     cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
#     daiToken.approve(accounts[1], amount, {'from': accounts[0]})

#     cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})
#     daiToken.transfer(accounts[1], amount, {'from': accounts[0]})

#     dai_balance = daiToken.balanceOf(accounts[1])
#     cubo_balance = cuboToken.balanceOf(accounts[1])

#     cuboToken.approve(daoContract, dai_balance, {'from': accounts[1]})
#     daiToken.approve(daoContract, cubo_balance, {'from': accounts[1]})
    
#     daoContract.mintNode(accounts[1], cubo_balance, dai_balance, 0, {'from': accounts[1]})
    
#     final_nodes_count = daoContract.getTotalNodes({'from': accounts[0]})
#     assert final_nodes_count == initial_nodes_count + 1
