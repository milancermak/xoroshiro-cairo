import pytest

from conftest import SEED

U64 = 2**64-1
STATE = (0, 0)

@pytest.mark.asyncio
async def test_next(x128_ss):

    s0 = splitmix64(SEED)
    s1 = splitmix64(s0)
    global STATE
    STATE = (s0, s1)

    def rotl(x, k):
        return (x << k) | (x >> (64 - k))

    def next():
        global STATE
        s0, s1 = STATE
        result = (rotl(s0 * 5, 7) * 9) & U64

        s1 ^= s0
        new_s0 = (rotl(s0, 24) ^ s1 ^ (s1 << 16)) & U64
        new_s1 = (rotl(s1, 37)) & U64
        STATE = (new_s0, new_s1)
        return result

    for r in range(1000):
        tx = await x128_ss.next().invoke()
        r = next()
        assert tx.result.rnd == r


@pytest.mark.asyncio
async def test_rotl(x128_ss_test):
    for (x, k) in [(1, 0), (1, 1), (2**64, 63), (2**64, 64), (2**123, 64)]:
        tx = await x128_ss_test.test_rotl(x, k).call()
        r = (x << k) | (x >> (64 - k))
        assert tx.result.out == r


# https://xoshiro.di.unimi.it/splitmix64.c
def splitmix64(x):
    U64 = 2**64-1

    z = x + 0x9e3779b97f4a7c15
    z &= U64
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9
    z &= U64
    z = (z ^ (z >> 27)) * 0x94d049bb133111eb
    z &= U64
    return (z ^ (z >> 31)) & U64


@pytest.mark.asyncio
async def test_splitmix64(x128_ss_test):
    for x in (0, 1, 2**64-1):
        tx = await x128_ss_test.test_splitmix64(x).call()
        assert tx.result.out == splitmix64(x)


@pytest.mark.asyncio
async def test_rshift(x128_ss_test):
    test_cases = [
        (1, 0),
        (1, 1),
        (2**127, 20),
        (2**128+1, 31),
        (2**128+1, 32),
        (2**192+2**30, 45),
        (2**250+2**20, 123)
    ]
    for (v, b) in test_cases:
        tx = await x128_ss_test.test_rshift(v, b).call()
        assert tx.result.out == v >> b
