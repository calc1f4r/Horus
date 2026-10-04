---
# Core Classification
protocol: Zealous
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62429
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Zealous.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[ZLS1-3] An attacker can set the exchange rate of ZEALInfinityPool to a very large or unlimited value

### Overview


This bug report discusses a medium severity issue in the ZEALInfinityPool contract. The problem occurs in two specific areas of the code and allows an attacker to manipulate the exchange rate between staked Zeal tokens and minted xZeal tokens. This can lead to a denial-of-service (DoS) attack, where the attacker can inflate the exchange rate and prevent others from staking into the contract. The report suggests resetting the `highestExchangeRate` variable to its default value when the total supply returns to zero as a possible solution. The bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** contracts/ZEALInfinityPool.sol#L192-L194
contracts/ZEALInfinityPool.sol#L85-L99

**Description:** In the ZEALInfinityPool contract, the exchange rate between staked Zeal tokens and minted xZeal tokens always increases, using the `highestExchangeRate` variable as a minimum bound.
```
function getExchangeRate() public view returns (uint256) {
    uint256 xSupply = xZealToken.totalSupply();
    if (xSupply == 0) {
        return highestExchangeRate; // Return highest rate if no supply
    }
    uint256 currentRate = (totalStaked + totalRewards).mulDiv(
        PRECISION_FACTOR,
        xSupply
    );

    return
        currentRate > highestExchangeRate
            ? currentRate
            : highestExchangeRate;
}
```
```
function stake(uint256 _amount) external nonReentrant {
    ...
    if (xSupply == 0) {
        currentRate = PRECISION_FACTOR;
    } else {
        currentRate = (totalStaked + totalRewards).mulDiv(
            PRECISION_FACTOR,
            xSupply
        );
    }

    currentRate = currentRate > highestExchangeRate
        ? currentRate
        : highestExchangeRate;
    ...
```
However, even when the current supply is zero, the contract still uses the previous `highestExchangeRate` as the minimum bound. This allows an attacker to repeatedly stake and unstake when the supply is zero, inflating the exchange rate, especially when rewards are added. 

With no cost, the attacker can inflate the exchange rate to an extremely large or even unlimited value, effectively preventing others from staking into the contract (DoS).

Example:

1. Initially, `currentRate = highestExchangeRate = PRECISION_FACTOR` (1e18).
The attacker stakes 1e18 Zeal tokens and receives 1e18 xZeal shares.

2. The attacker then adds 1e18 Zeal tokens as rewards. Now, `highestExchangeRate = currentRate = 2e18`.
The attacker unstakes 1e18 xZeal shares and receives the full 2e18 Zeal tokens, because the exchange rate for unstaking is set to `highestExchangeRate` when the remaining xZeal supply is zero.

3. Next, the attacker stakes 1e18 Zeal tokens again but receives only 0.5e18 xZeal shares, since the `highestExchangeRate` is now 2e18.
The attacker can then add 1e18 Zeal tokens as rewards and unstake the 0.5e18 xZeal shares, doubling the exchange rate to 4e18.

4. By repeating this process (with just 2e18 Zeal tokens), the attacker can increase the `highestExchangeRate` to a very large value, making it so that any new Zeal token stakes will receive zero shares -  effectively causing a denial-of-service (DoS) on the pool.

**Remediation:**  Consider reseting `highestExchangeRate` to its default value whenever the total supply returns to zero.

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Zealous |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Zealous.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

