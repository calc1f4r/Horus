---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 406
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-gro-protocol-contest
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/6

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - overflow/underflow

protocol_categories:
  - dexes
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - gpersoon
---

## Vulnerability Title

[H-01] implicit underflows

### Overview


This bug report is about a vulnerability in the code of a software system. The vulnerability is caused by underflows that are converted via a typecast afterwards to the expected value. If solidity 0.8.x is used, then the code will revert. This vulnerability appears when int256(a-b) and int256(-x) are used, where a and b are uint and x is a uint. It is recommended to replace int256(a-b) with int256(a)-int256(b) and int256(-x) with -int256(x) as mitigation steps. This should be done to avoid any issues when moving to solidity 0.8.x.

### Original Finding Content

_Submitted by gpersoon, also found by cmichel_

There are a few underflows that are converted via a typecast afterwards to the expected value. If solidity 0.8.x would be used, then the code would revert.
* `int256(a-b)` where a and b are uint: For example, if `a=1` and `b=2`, then the intermediate result would be `uint(-1) == 2**256-1`
* `int256(-x)` where x is a uint. For example, if `x=1`, then the intermediate result would be `uint(-1) == 2**256-1`

It's better not to have underflows by using the appropriate typecasts. This is especially relevant when moving to solidity 0.8.x.

From `Exposure.sol` [L178](https://github.com/code-423n4/2021-06-gro/blob/main/contracts/insurance/Exposure.sol#L178):
```solidity
function sortVaultsByDelta(..)
..
    for (uint256 i = 0; i < N_COINS; i++) {
        // Get difference between vault current assets and vault target
        int256 delta = int256(unifiedAssets[i] - unifiedTotalAssets.mul(targetPercents[i]).div(PERCENTAGE_DECIMAL_FACTOR)); // underflow in intermediate result
```

From `PnL.sol` [L112](https://github.com/code-423n4/2021-06-gro/blob/main/contracts/pnl/PnL.sol#L112):
```solidity
 function decreaseGTokenLastAmount(bool pwrd, uint256 dollarAmount, uint256 bonus)...
..
 emit LogNewGtokenChange(pwrd, int256(-dollarAmount)); // underflow in intermediate result
```

From `Buoy3Pool.sol` [L87](https://github.com/code-423n4/2021-06-gro/blob/main/contracts/pools/oracle/Buoy3Pool.sol#L87):
```solidity
function safetyCheck() external view override returns (bool) {
    ...
        _ratio = abs(int256(_ratio - lastRatio[i])); // underflow in intermediate result
```

Recommend replacing `int256(a-b)` with `int256(a)-int256(b)`, and replacing `int256(-x)` with `-int256(x)`

**[kristian-gro (Gro) confirmed but disagreed with severity](https://github.com/code-423n4/2021-06-gro-findings/issues/6#issuecomment-886260551):**
> Confirmed and We've mitigated this issue in our release version.

**[ghoul-sol (Judge) commented](https://github.com/code-423n4/2021-06-gro-findings/issues/6#issuecomment-886260551):**
 > Majority of overflow listed above seems low risk with one exception of `safetyCheck`. Underflow is a real risk here.`safetyCheck` is run every time a deposit is made. Ratios can change and the change does not need to be substantial for it to overflow. For that reason it's a high risk.




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | cmichel, gpersoon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/6
- **Contest**: https://code4rena.com/contests/2021-07-gro-protocol-contest

### Keywords for Search

`Overflow/Underflow`

