%lang starknet

from contracts.xoroshiro128_starstar import rotl, rshift, splitmix64
from starkware.cairo.common.cairo_builtins import BitwiseBuiltin

@view
func test_rotl{bitwise_ptr : BitwiseBuiltin*, range_check_ptr}(x : felt, k : felt) -> (out : felt):
    let (out) = rotl(x, k)
    return (out)
end

@view
func test_rshift{bitwise_ptr : BitwiseBuiltin*, range_check_ptr}(v : felt, b : felt) -> (
    out : felt
):
    let (out) = rshift(v, b)
    return (out)
end

@view
func test_splitmix64{bitwise_ptr : BitwiseBuiltin*, range_check_ptr}(x : felt) -> (out : felt):
    let (out) = splitmix64(x)
    return (out)
end
