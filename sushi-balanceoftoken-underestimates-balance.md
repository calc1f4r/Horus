---
# Core Classification
protocol: PoolTogether — Sushi and Yearn V2 Yield Sources
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13372
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/pooltogether-sushi-and-yearn-v2-yield-sources/
github_link: none

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
  - dexes
  - cdp
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Heiko Fisch
  -  Sergii Kravchenko

---

## Vulnerability Title

Sushi: balanceOfToken underestimates balance

### Overview


The bug report describes an issue with the `balanceOfToken` computation in the SushiYieldSource.sol contract. This computation can underestimate the current balance of asset tokens, as it is too pessimistic. The report provides a code snippet to illustrate the issue, and the recommended solution is to use a different formula to calculate the balance of asset tokens. This formula takes into account the amount of SUSHI that the address in question could withdraw directly from the SushiBar, based on their amount of shares. This formula should replace the current `balanceOfToken` computation to ensure that the current balance of asset tokens is accurately calculated.

### Original Finding Content

#### Description


The `balanceOfToken` computation is too pessimistic, i.e., it can underestimate the current balance slightly.


**code/sushi-pooltogether/contracts/SushiYieldSource.sol:L29-L45**



```
/// @notice Returns the total balance (in asset tokens). This includes the deposits and interest.
/// @return The underlying balance of asset tokens
function balanceOfToken(address addr) public override returns (uint256) {
    if (balances[addr] == 0) return 0;
    ISushiBar bar = ISushiBar(sushiBar);

    uint256 shares = bar.balanceOf(address(this));
    uint256 totalShares = bar.totalSupply();

    uint256 sushiBalance =
        shares.mul(ISushi(sushiAddr).balanceOf(address(sushiBar))).div(
            totalShares
        );
    uint256 sourceShares = bar.balanceOf(address(this));

    return (balances[addr].mul(sushiBalance).div(sourceShares));
}

```
First, it calculates the amount of SUSHI that “belongs to” the yield source contract (`sushiBalance`), and then it determines the fraction of *that amount* that would be owed to the address in question. However, the “belongs to” above is a purely theoretical concept; it never happens that the yield source contract as a whole redeems and then distributes that amount among its shareholders; instead, if a shareholder redeems tokens, their request is passed through to the `SushiBar`.
So in reality, there’s no reason for this two-step process, and the holder’s balance of SUSHI is more accurately computed as `balances[addr].mul(ISushi(sushiAddr).balanceOf(address(sushiBar))).div(totalShares)`, which can be greater than what `balanceOfToken` currently returns. Note that this is the amount of SUSHI that `addr` could withdraw directly from the `SushiBar`, based on their amount of shares. Observe also that if we sum these numbers up over all holders in the yield source contract, the result is smaller than or equal to `sushiBalance`. So the sum still doesn’t exceed what “belongs to” the yield source contract.


#### Recommendation


The `balanceOfToken` function should use the formula above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | PoolTogether — Sushi and Yearn V2 Yield Sources |
| Report Date | N/A |
| Finders | Heiko Fisch,  Sergii Kravchenko
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/pooltogether-sushi-and-yearn-v2-yield-sources/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

