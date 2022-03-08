#!/usr/bin/python3
import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass

@pytest.fixture
def cuboToken(Cubo, accounts):
    return Cubo.deploy({'from': accounts[0]})

@pytest.fixture
def daiToken(Dai, accounts):
    return Dai.deploy({'from': accounts[0]})

@pytest.fixture()
def daoContract(cuboToken, daiToken, CuboDaoV1, accounts):
    dao = CuboDaoV1.deploy(cuboToken, daiToken,{'from': accounts[0]})
    cuboToken.setDaoContract(dao, {'from': accounts[0]})
    return dao
   
@pytest.fixture()
def coneVaultContract(accounts, daoContract, daiToken, cuboToken, ConeVaultV1, ):
    return ConeVaultV1.deploy("Test Vault", daoContract, cuboToken, daiToken, 0, 100*10**18, 100*10**18, 10, accounts[9],{'from': accounts[0]})
