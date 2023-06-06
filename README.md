# xoroshiro-cairo

A [xoroshiro128**](https://prng.di.unimi.it/) pseudorandom number generator implementation in Cairo.

## Usage

You can use the deployed onchain contract via the following interface or install it as a library via Scarb.

### Interface

```rust
#[abi]
trait IXoroshiro {
    fn next() -> u128;
}
```

### Addresses

The contract has been declared and deploy on both testnet and mainnet. Class hash and addresses are the same on both networks:

Class hash: `0x1ef52fac5efec1fe792b73d7fdcc0cba30dc1b166466ddaa5aa79a126b6aa44`

Deployed contract (`seed = 42`) address: `0x6f6ad3411cfe6812bce43ffc1ad6ab1f2cd590f37abf83c058d3e57368cc300`

#### Testnet

[declare TX](https://testnet.starkscan.co/tx/0x62aefa6f5d91b79922b99669afc786a3b0a2003d9c29b997ec4b1a06c3566a9)

[deploy TX](https://testnet.starkscan.co/tx/0x20cbcd737cb81f756dfb3bd9ca75194b002c077ca9124c9510a86c9f617bf25)

[contract](https://testnet.starkscan.co/contract/0x06f6ad3411cfe6812bce43ffc1ad6ab1f2cd590f37abf83c058d3e57368cc300)

#### Mainnet

[declare TX](https://starkscan.co/tx/0x609db6a72e0b0be6ad3075531314ae7349858cd785c418d0fbfbf597c4c6a7f)

[deploy TX](https://starkscan.co/tx/0x17ab4baf84079fdf3dbc8822fc26e05534fd4a431af3c88b0f852ee67db2a89)

[contract](https://starkscan.co/contract/0x06f6ad3411cfe6812bce43ffc1ad6ab1f2cd590f37abf83c058d3e57368cc300)
