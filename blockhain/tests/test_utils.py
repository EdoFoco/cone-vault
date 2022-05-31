def transfer_funds(sender, receiver, amount, token):
    token.approve(receiver, amount, {'from': sender})
    token.transfer(receiver, amount, {'from': sender})

