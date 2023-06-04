#[abi]
trait IXoroshiro {
    fn next() -> u128;
}

#[contract]
mod Xoroshiro {
    const U64: u128 = 0xffffffffffffffff_u128; // 2**64-1

    struct Storage {
        s0: u128,
        s1: u128
    }

    #[constructor]
    fn constructor(seed: u128) {
        let s0 = splitmix(seed);
        let s1 = splitmix(s0);

        s0::write(s0);
        s1::write(s1);
    }

    #[external]
    fn next() -> u128 {
        let s0 = s0::read();
        let s1 = s1::read();

        let result = (rotl(s0 * 5, 7) * 9) & U64;

        let s1 = (s1 ^ s0) & U64;
        s0::write((rotl(s0, 24) ^ s1 ^ (s1 * 65536)) & U64);
        s1::write((rotl(s1, 37) & U64));
        result
    }

    fn rotl(x: u128, k: u128) -> u128 {
        assert(k <= 64, 'invalid k');
        // (x << k) | (x >> (64 - k))
        (x * pow2(k)) | rshift(x, 64 - k)
    }

    // https://xoshiro.di.unimi.it/splitmix64.c
    // uint64_t z = (x += 0x9e3779b97f4a7c15);
    // z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9;
    // z = (z ^ (z >> 27)) * 0x94d049bb133111eb;
    // return z ^ (z >> 31);
    fn splitmix(x: u128) -> u128 {
        let z = (x + 0x9e3779b97f4a7c15) & U64;
        let z = ((z ^ rshift(z, 30)) * 0xbf58476d1ce4e5b9) & U64;
        let z = ((z ^ rshift(z, 27)) * 0x94d049bb133111eb) & U64;
        (z ^ rshift(z, 31)) & U64
    }

    #[inline(always)]
    fn rshift(v: u128, b: u128) -> u128 {
        v / pow2(b)
    }

    fn pow2(mut i: u128) -> u128 {
        let mut p = 1;
        loop {
            if i == 0 {
                break p;
            }
            p *= 2;
            i -= 1;
        }
    }
}

#[cfg(test)]
mod test {
    use array::{ArrayTrait, SpanTrait};
    use option::OptionTrait;
    use starknet::{class_hash_try_from_felt252, ContractAddress, deploy_syscall, SyscallResultTrait};
    use traits::Default;

    use super::{IXoroshiroDispatcher, IXoroshiroDispatcherTrait, Xoroshiro};

    fn deploy(seed: felt252) -> ContractAddress {
        let mut calldata = Default::default();
        calldata.append(seed);

        let contract = class_hash_try_from_felt252(Xoroshiro::TEST_CLASS_HASH).unwrap();
        let (xoroshiro, _) = deploy_syscall(contract, 0, calldata.span(), false).unwrap_syscall();

        xoroshiro
    }

    #[test]
    #[available_gas(10000000000)]
    fn test_next_20() {
        let xoroshiro = IXoroshiroDispatcher { contract_address: deploy(42) };

        assert(xoroshiro.next() == 7631449856891430058, 'next 1');
        assert(xoroshiro.next() == 13383391556906898403, 'next 2');
        assert(xoroshiro.next() == 968208867642205398, 'next 3');
        assert(xoroshiro.next() == 18175738666922262653, 'next 4');
        assert(xoroshiro.next() == 10565592856649446153, 'next 5');
        assert(xoroshiro.next() == 7599944514057266308, 'next 6');
        assert(xoroshiro.next() == 6033996411961164690, 'next 7');
        assert(xoroshiro.next() == 9860751469970290964, 'next 8');
        assert(xoroshiro.next() == 14588874553204967316, 'next 9');
        assert(xoroshiro.next() == 17224833315124355019, 'next 10');
        assert(xoroshiro.next() == 13825518728669172250, 'next 11');
        assert(xoroshiro.next() == 10813161253949910651, 'next 12');
        assert(xoroshiro.next() == 3278939010906543816, 'next 13');
        assert(xoroshiro.next() == 114592805787241389, 'next 14');
        assert(xoroshiro.next() == 2536017247944469090, 'next 15');
        assert(xoroshiro.next() == 3316880442200810148, 'next 16');
        assert(xoroshiro.next() == 842976429519100211, 'next 17');
        assert(xoroshiro.next() == 15595496597317679978, 'next 18');
        assert(xoroshiro.next() == 12835187214640123272, 'next 19');
        assert(xoroshiro.next() == 15140784658950556840, 'next 20');
    }

    #[test]
    #[available_gas(10000000000000)]
    fn test_successful_10K() {
        let xoroshiro = IXoroshiroDispatcher { contract_address: deploy(42) };
        let mut i = 10000;
        loop {
            if i == 0 {
                break;
            }
            xoroshiro.next();
            i -= 1;
        };
    }
}
