---
# Core Classification
protocol: Thruster
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30612
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-thruster
source_link: https://code4rena.com/reports/2024-02-thruster
github_link: none

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
finders_count: 0
finders:
---

## Vulnerability Title

[L-11] Thruster pairs are vulnerable to first-depositor price manipulation

### Overview

See description below for full details.

### Original Finding Content


### Instances(1)

Compared to ThrusterPool.sol, ThrusterPair.sol follows UniswapV2 logic and allows any reserve ratio to be deposited by the first depositor.

Due to ThrusterPair.sol only allows depositing liquidity at the existing reserve ratio, the second depositor might be vulnerable to depositing reserves at an unfavorable ratio, which allows the first depositor to profit through back-running unsuspected depositors with swap tx for profits.

As an example, the first depositor might deposit a cheap token(tokenA) and WETH at a ratio (1:1) which inflates tokenA's price in the pool. The first depositor can deposit dust amount of both just enough to pass `MINIMUM_LIQUIDITY` threshold (e.g. 1100 wei tokenA: 1100 wei WETH). If the second depositor is not as technically proficient, they might simply deposit both token at the normal price (e.g. 1000 ether tokenA : 1 ether WETH). This would allow first depositor to back-run with a swap tx to swap tokenA for WETH taking advantage of the inflated price of tokenA and increased liquidity and realizing a profit.

There could be other scenarios of similar attacks, including the pool deployer maliciously creating a pool and atomically first depositing with a low but unbalanced reserve ratio. 

Note that price manipulations are also possible at later deposits as long as the pair liquidity is low enough for the attacker.

```solidity
//thruster-protocol/thruster-cfmm/contracts/ThrusterPair.sol
    function mint(address to) external lock returns (uint256 liquidity) {
...
        if (_totalSupply == 0) {
            liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
            _mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens
        } else {
            liquidity = Math.min(
                amount0.mul(_totalSupply) / _reserve0,
                amount1.mul(_totalSupply) / _reserve1
            );
        }
        require(liquidity > 0, "ThrusterPair: INSUFFICIENT_LIQUIDITY_MINTED");
        _mint(to, liquidity);
...
```
(https://github.com/code-423n4/2024-02-thruster/blob/3896779349f90a44b46f2646094cb34fffd7f66e/thruster-protocol/thruster-cfmm/contracts/ThrusterPair.sol#L151-L158)

### Recommendations

Might consider allowing pool deployers to suggest a reasonable reserve ratio at the pair initialization process `initialize()`. Although this will not prevent pool deployer from being malicious, this can mitigate certain price manipulation attempts.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Thruster |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-thruster
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-02-thruster

### Keywords for Search

`vulnerability`

