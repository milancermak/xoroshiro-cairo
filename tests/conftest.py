import asyncio
import os

import pytest
from starkware.starknet.services.api.contract_class import ContractClass
from starkware.starknet.compiler.compile import compile_starknet_files
from starkware.starknet.testing.starknet import Starknet, StarknetContract


def here() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def contract_path(contract_name: str) -> str:
    return os.path.join(here(), "..", "contracts", contract_name)


def compile_contract(contract_name: str) -> ContractClass:
    contract_src = contract_path(contract_name)
    return compile_starknet_files(
        [contract_src],
        debug_info=True,
        disable_hint_validation=True,
        cairo_path=[os.path.join(here(), "..", "contracts")]
    )


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(scope="module")
async def starknet() -> Starknet:
    starknet = await Starknet.empty()
    return starknet

@pytest.fixture
async def account_factory(starknet):

    account_path = os.path.join(here(), "mocks", "account", "Account.cairo")
    cairo_path = os.path.join(here(), "mocks", "account")
    account_contract = compile_starknet_files([account_path], debug_info=True, cairo_path=[cairo_path])

    async def account_for_signer(signer):
        return await starknet.deploy(contract_class=account_contract, constructor_calldata=[signer.public_key])

    yield account_for_signer


SEED = 42


@pytest.fixture(scope="module")
async def x128_ss(starknet) -> StarknetContract:
    contract = compile_contract("xoroshiro128_starstar.cairo")
    return await starknet.deploy(contract_class=contract, constructor_calldata=[SEED])


@pytest.fixture(scope="module")
async def x128_ss_test(starknet) -> StarknetContract:
    contract = compile_contract("xoroshiro128_starstar_test.cairo")
    return await starknet.deploy(contract_class=contract,
        # no idea why, but the constructor_calldata has to be set
        constructor_calldata=[SEED]
    )
