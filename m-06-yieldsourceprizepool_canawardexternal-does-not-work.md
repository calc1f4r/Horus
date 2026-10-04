---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25481
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-pooltogether
source_link: https://code4rena.com/reports/2021-06-pooltogether
github_link: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/92

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-06] `YieldSourcePrizePool_canAwardExternal` does not work

### Overview


A bug has been reported in the code of the YieldSourcePrizePool_canAwardExternal function. This function is intended to disallow awarding the interest-bearing token of the yield source, such as aTokens, cTokens and yTokens. However, the code checks `_externalToken != address(yieldSource)` where `yieldSource` is the actual yield strategy contract and not the strategy's interest-bearing token. This means the function does not work as expected and it might be possible to award the interest-bearing token which could lead to errors and loss of funds when trying to redeem underlying. 

The bug report also suggests adding a function to return the interest-bearing token, similar to `depositToken()` which retrieves the underlying token. A potential solution of adding an extra check to the `_canAwardExternal` function has been discussed, however the yield source needs to be asked in order to know what token the prize pool may or may not hold. In the end, it was decided to leave the function as-is.

### Original Finding Content

_Submitted by cmichel_

The idea of `YieldSourcePrizePool_canAwardExternal` seems to be to disallow awarding the interest-bearing token of the yield source, like aTokens, cTokens, yTokens.

> "@dev Different yield sources will hold the deposits as another kind of token: such a Compound's cToken.  The prize strategy should not be allowed to move those tokens."

However, the code checks `_externalToken != address(yieldSource)` where `yieldSource` is the actual yield strategy contract and not the strategy's interest-bearing token.
Note that the `yieldSource` is usually not even a token contract except for `ATokenYieldSource` and `YearnV2YieldSource`.

The `_canAwardExternal` does not work as expected. It might be possible to award the interest-bearing token which would lead to errors and loss of funds when trying to redeem underlying.

There doesn't seem to be a function to return the interest-bearing token. It needs to be added, similar to `depositToken()` which retrieves the underlying token.

**[asselstine (PoolTogether) acknowledged](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/92#issuecomment-868859317):**
 > This is an interesting one:
>
> - the yield source interface does not require the deposit be tokenized; the implementation is entirely up to the yield source.
> - the _canAwardExternal is a legacy of older code.  Since it had to be included it was set to assume the yield source was tokenized.
>
> Since yield sources are audited and analyzed, I think this is a pretty low risk.  Additionally, not all of the yield sources are tokenized (Badger and Sushi are not), so it isn't a risk for them.
>
> We could have `canAwardExternal` on the yield source itself, but it would add gas overhead.
>

**[aodhgan (PoolTogether) commented](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/92#issuecomment-873106239):**
 > Could we add an check -
> `
> function _canAwardExternal(address _externalToken) internal override view returns (bool) {
> return _externalToken != address(yieldSource) && _externalToken != address(yieldSource.depositToken())
> }`

**[asselstine (PoolTogether) commented](https://github.com/code-423n4/2021-06-pooltogether-findings/issues/92#issuecomment-874342323):**
 > We could add another check, but it's still arbitrary.  The point is that the yield source knows what token the prize pool may or may not hold, so without asking the yield source it's just a guess.
>
> Let's leave it as-is



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-pooltogether
- **GitHub**: https://github.com/code-423n4/2021-06-pooltogether-findings/issues/92
- **Contest**: https://code4rena.com/reports/2021-06-pooltogether

### Keywords for Search

`vulnerability`

