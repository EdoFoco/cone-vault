#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, cuboToken):
    receiver_balance = cuboToken.balanceOf(accounts[1])
    amount = cuboToken.balanceOf(accounts[0]) // 4

    cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(accounts, cuboToken):
    total_supply = cuboToken.totalSupply()
    amount = cuboToken.balanceOf(accounts[0])

    cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert cuboToken.totalSupply() == total_supply


def test_returns_true(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])
    tx = cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])
    receiver_balance = cuboToken.balanceOf(accounts[1])

    cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[0]) == 0
    assert cuboToken.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_tokens(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    receiver_balance = cuboToken.balanceOf(accounts[1])

    cuboToken.transfer(accounts[1], 0, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance
    assert cuboToken.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(accounts, cuboToken):
    sender_balance = cuboToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    cuboToken.transfer(accounts[0], amount, {'from': accounts[0]})

    assert cuboToken.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(accounts, cuboToken):
    balance = cuboToken.balanceOf(accounts[0])

    with brownie.reverts():
        cuboToken.transfer(accounts[1], balance + 1, {'from': accounts[0]})


def test_transfer_event_fires(accounts, cuboToken):
    amount = cuboToken.balanceOf(accounts[0])
    tx = cuboToken.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]
