import asyncio
import os

import pytest
from starkware.starknet.services.api.contract_definition import ContractDefinition
from starkware.starknet.compiler.compile import compile_starknet_files
from starkware.starknet.testing.starknet import Starknet, StarknetContract


def contract_path(contract_name: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, "..", "contracts", contract_name)


def compile_contract(contract_name: str) -> ContractDefinition:
    contract_src = contract_path(contract_name)
    return compile_starknet_files(
        [contract_src],
        debug_info=True,
        disable_hint_validation=True,
        cairo_path=["../contracts/"]
    )


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(scope="module")
async def starknet() -> Starknet:
    starknet = await Starknet.empty()
    return starknet


SEED = 42


@pytest.fixture(scope="module")
async def x128_ss(starknet) -> StarknetContract:
    contract = compile_contract("xoroshiro128_starstar.cairo")
    return await starknet.deploy(contract_def=contract, constructor_calldata=[SEED])


@pytest.fixture(scope="module")
async def x128_ss_test(starknet) -> StarknetContract:
    contract = compile_contract("xoroshiro128_starstar_test.cairo")
    return await starknet.deploy(contract_def=contract,
        # no idea why, but the constructor_calldata has to be set
        constructor_calldata=[SEED]
    )
