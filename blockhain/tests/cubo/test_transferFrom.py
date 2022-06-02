#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, cuboToken):
    receiver_balance = cuboToken.balanceOf(accounts[2])
    amount = cuboToken.balanceOf(accounts[0]) // 4

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[2]) == receiver_balance + amount


def test_caller_balance_not_affected(accounts, cuboToken):
    caller_balance = cuboToken.balanceOf(accounts[1])
    amount = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[1]) == caller_balance


def test_caller_approval_affected(accounts, cuboToken):
    approval_amount = cuboToken.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    cuboToken.approve(accounts[1], approval_amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert cuboToken.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(accounts, cuboToken):
    approval_amount = cuboToken.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    cuboToken.approve(accounts[1], approval_amount, {'from': accounts[0]})
    cuboToken.approve(accounts[2], approval_amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert cuboToken.allowance(accounts[0], accounts[2]) == approval_amount


def test_total_supply_not_affected(accounts, cuboToken):
    total_supply = cuboToken.totalSupply()
    amount = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert cuboToken.totalSupply() == total_supply


def test_returns_true(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])
    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    tx = cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])
    receiver_balance = cuboToken.balanceOf(accounts[2])

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[0]) == 0
    assert cuboToken.balanceOf(accounts[2]) == receiver_balance + amount


def test_transfer_zero_tokens(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    receiver_balance = cuboToken.balanceOf(accounts[2])

    cuboToken.approve(accounts[1], sender_balance, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance
    assert cuboToken.balanceOf(accounts[2]) == receiver_balance


def test_transfer_zero_tokens_without_approval(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    receiver_balance = cuboToken.balanceOf(accounts[2])

    cuboToken.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance
    assert cuboToken.balanceOf(accounts[2]) == receiver_balance


def test_insufficient_balance(accounts, cuboToken):
    balance = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], balance + 1, {'from': accounts[0]})
    with brownie.reverts():
        cuboToken.transferFrom(accounts[0], accounts[2], balance + 1, {'from': accounts[1]})


def test_insufficient_approval(accounts, cuboToken):
    balance = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], balance - 1, {'from': accounts[0]})
    with brownie.reverts():
        cuboToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_no_approval(accounts, cuboToken):
    balance = cuboToken.balanceOf(accounts[0])

    with brownie.reverts():
        cuboToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_revoked_approval(accounts, cuboToken):
    balance = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], balance, {'from': accounts[0]})
    cuboToken.approve(accounts[1], 0, {'from': accounts[0]})

    with brownie.reverts():
        cuboToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_transfer_to_self(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    cuboToken.approve(accounts[0], sender_balance, {'from': accounts[0]})
    cuboToken.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance
    assert cuboToken.allowance(accounts[0], accounts[0]) == sender_balance - amount


def test_transfer_to_self_no_approval(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])

    with brownie.reverts():
        cuboToken.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})


def test_transfer_event_fires(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])

    cuboToken.approve(accounts[1], amount, {'from': accounts[0]})
    tx = cuboToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert len(tx.events) == 2
    assert tx.events["Transfer"].values() == [accounts[0], accounts[2], amount]
