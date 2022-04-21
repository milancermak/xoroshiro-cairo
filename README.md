# xoroshiro-cairo

![tests](https://github.com/milancermak/xoroshiro-cairo/actions/workflows/tests.yml/badge.svg)

A [xoroshiro128**](https://prng.di.unimi.it/) pseudorandom number generator implementation in Cairo.

## Deploying

Presuming you have [nile](https://github.com/OpenZeppelin/nile) installed, you can `compile` and `deploy` the contract. You'll need a single number (a seed) that's passed in as an input argument to the constructor:

```sh
nile compile
nile deploy --network goerli xoroshiro128_starstar 161803398
```

An instance of this contract has been deployed at [`0x06c4cab9afab0ce564c45e85fe9a7aa7e655a7e0fd53b7aea732814f3a64fbee`](https://goerli.voyager.online/contract/0x06c4cab9afab0ce564c45e85fe9a7aa7e655a7e0fd53b7aea732814f3a64fbee#transactions), you can use it as well.

## Usage

You can probe the deployed contract on Goerli for a random number inside your Starknet contract:

```
%lang starknet

const XOROSHIRO_ADDR = 0x06c4cab9afab0ce564c45e85fe9a7aa7e655a7e0fd53b7aea732814f3a64fbee

@contract_interface
namespace IXoroshiro:
    func next() -> (rnd : felt):
    end
end

@external
func get_next_rnd{syscall_ptr : felt*, range_check_ptr}() -> (rnd : felt):
    let (rnd) = IXoroshiro.next(contract_address=XOROSHIRO_ADDR)
    return (rnd)
end
```

The contract has not been audited, use it at your own discresion.
