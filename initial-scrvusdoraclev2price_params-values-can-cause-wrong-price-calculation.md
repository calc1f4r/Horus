---
# Core Classification
protocol: Storage Proofs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55733
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm7m0p7v40000bclqs4jsmnhd
source_link: none
github_link: https://github.com/CodeHawks-Contests/2025-03-curve

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bakhankov
---

## Vulnerability Title

Initial ScrvusdOracleV2::price_params values can cause wrong price calculation

### Overview

See description below for full details.

### Original Finding Content

## Summary

The initial values of `price_params` in `ScrvusdOracleV2` constructor are hardcoded to `total_idle=1` and `total_supply=1`. This can cause wrong price calculation in `price_v2()` and `raw_price()` functions. Wich can lead to opportunity to trade tokens at significantly lower price than expected.

## Vulnerability Details

Hardcoded initial values of `price_params` in `ScrvusdOracleV2` constructor can cause wrong price calculation in `price_v2()` and `raw_price()` functions.

`contracts/scrvusd/oracles/ScrvusdOracleV2.vy`

```python
@deploy
def __init__(_initial_price: uint256):
    """
    @param _initial_price Initial price of asset per share (10**18)
    """
    self.last_prices = [_initial_price, _initial_price, _initial_price]
    self.last_update = block.timestamp

    # initial raw_price is 1
    self.profit_max_unlock_time = 7 * 86400  # Week by default
    self.price_params = PriceParams(
        total_debt=0,
@>      total_idle=1,
@>      total_supply=1,
        full_profit_unlock_date=0,
        profit_unlocking_rate=0,
        last_profit_update=0,
        balance_of_self=0,
    )
```

If the oracle smart contract is deployed much later than the scrvUSD contract is operational, this will result in a temporary discrepancy in the price reported by the oracle. The `price_v2()` function will return the initial `_initial_price` value, while the `raw_price()` function will return `1*10**18`. This discrepancy will be resolved after the first price update, but until then, the price reported by the oracle will be incorrect. What much worse, if the `max_price_increment` is updated before the first price update, the discrepancy will affect the `price_v2()`.

## Impact

Such discrepancy can lead to an opportunity to trade tokens at significantly lower price than expected. The more time passes between the scrvUSD contract deployment and the oracle contract deployment, the more significant gains can be made by exploiting this vulnerability.

## PoC

Put the following code in a file `tests/scrvusd/oracle/unitary/test_v2.py`

```python
@pytest.fixture(scope="module")
def soracle(admin):
    with boa.env.prank(admin):
        # assume we are deploying the oracle for the new blockchain after years of scrvUSD existence,
        # so the price reached 4 crvUSD per scrvUSD, _initial_price is 4*10**18
        contract = boa.load("contracts/scrvusd/oracles/ScrvusdOracleV2.vy", 4*10**18)
    return contract


def test_initial_price_at_later_oracle_deploy(soracle, verifier, admin):
    print("\n| where                      | price_v2()        | raw_price()       | block_number")
    # here price_v2() returns 4, but raw_price() returns 1
    price_v2, raw_price = soracle.price_v2(), soracle.raw_price()
    print("  on init                    ", price_v2, raw_price, boa.env.evm.patch.block_number)
    assert price_v2 == 4*10**18
    assert raw_price == 1*10**18  # incorrect

    # assume for some reason we want to increase the max_price_increment
    with boa.env.prank(admin):
        soracle.set_max_price_increment(10**18)
    
    # then if we do not update the price at the same block, the price at price_v2() will be inconsistent and equal to 1
    boa.env.time_travel(seconds=12)
    price_v2, raw_price = soracle.price_v2(), soracle.raw_price()
    print("  max_price_increment updated", price_v2, raw_price, boa.env.evm.patch.block_number)
    assert price_v2 == 1*10**18   # incorrect
    assert raw_price == 1*10**18  # incorrect

    # prepare the price parameters
    ts = boa.env.evm.patch.timestamp
    price_params = [
        0,                                # total_debt
        40000000000000000000000000,       # total_idle
        10000000000000000000000000,       # totalSupply
        ts + 500000,                      # full_profit_unlock_date
        5831137848451547566180476730,     # profit_unlocking_rate
        ts,                               # last_profit_update
        3000000000000000000000,           # balanceOf(self)
    ]

    with boa.env.prank(verifier):
        soracle.update_price(
            price_params,
            ts,
            boa.env.evm.patch.block_number,
        )

    # only after price update the raw_price() will be consistent and equal to 4
    # but price_v2() will still be inconsistent and equal to 1
    price_v2, raw_price = soracle.price_v2(), soracle.raw_price()
    print("  after update_price         ", price_v2, raw_price, boa.env.evm.patch.block_number)
    assert price_v2 == 1*10**18  # incorrect
    assert raw_price == 4*10**18

    # only at the next block the price_v2() will become consistent
    boa.env.time_travel(seconds=12)
    price_v2, raw_price = soracle.price_v2(), soracle.raw_price()
    print("  wait one block             ", price_v2, raw_price, boa.env.evm.patch.block_number)
    assert price_v2 > 4*10**18
    assert raw_price > 4*10**18

## run it with `-s` flag to see the print statements
## pytest tests/scrvusd/oracle/unitary/test_v2.py::test_initial_price_at_later_oracle_deploy -s

## stdout output:
#| where                      | price_v2()        | raw_price()       | block_number
## on init                     4000000000000000000 1000000000000000000 1
## max_price_increment updated 1000000000000000000 1000000000000000000 2
## after update_price          1000000000000000000 4000000000000000000 2
## wait one block              4000000027989461868 4000000027989461868 3

```

## Recommendations

Use `_initial_price` as value for initial `price_params` in `ScrvusdOracleV2` constructor.

```diff
@deploy
def __init__(_initial_price: uint256):
    """
    @param _initial_price Initial price of asset per share (10**18)
    """
    self.last_prices = [_initial_price, _initial_price, _initial_price]
    self.last_update = block.timestamp

    # initial raw_price is 1
    self.profit_max_unlock_time = 7 * 86400  # Week by default
    self.price_params = PriceParams(
        total_debt=0,
-       total_idle=1,
-       total_supply=1,
+       total_idle=_initial_price,
+       total_supply=10**18,
        full_profit_unlock_date=0,
        profit_unlocking_rate=0,
        last_profit_update=0,
        balance_of_self=0,
    )
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Storage Proofs |
| Report Date | N/A |
| Finders | bakhankov |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/CodeHawks-Contests/2025-03-curve
- **Contest**: https://codehawks.cyfrin.io/c/cm7m0p7v40000bclqs4jsmnhd

### Keywords for Search

`vulnerability`

