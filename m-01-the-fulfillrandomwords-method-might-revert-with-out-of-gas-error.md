---
# Core Classification
protocol: Bearcave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20612
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-BearCave.md
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
  - Pashov
---

## Vulnerability Title

[M-01] The `fulfillRandomWords` method might revert with out of gas error

### Overview


The `fulfillRandomWords` method in the HibernationDen contract has two potential issues. The first is that it calls the internal `_setFermentedJars` method which can require a lot of gas and cause the `fulfillRandomWords` method to revert, which is problematic for VRF integrations. The second is that it has an external call when the conditions `party.assetChainId != getChainId() && address(honeyJarPortal) != address(0)` and `address(this).balance != 0` are true. This is exploitable as anyone can send 1 wei of ETH into the contract, causing additional gas cost overhead and a cross-chain call that is likely to fail due to the `sendAmount` being rounded down to zero.

To rectify the issues, it is recommended to cache the randomness received and let an externally owned account make the `_setFermentedJars` call, as well as check that the balance is enough to do the `sendFermentedJars` call, not just that the balance is non-zero. The impact of these issues is high, as randomness won't be fulfilled, however the likelihood is low as it requires misconfiguration of gas.

### Original Finding Content

**Impact:**
High, as randomness won't be fulfilled

**Likelihood:**
Low, as it requires misconfiguration of gas

**Description**

The `fulfillRandomWords` method in `HibernationDen` calls the internal `_setFermentedJars` method which loops over the `fermentedJars` array and also has an external call. This is a potential problem as this code might require a lot of gas and make the `fulfillRandomWords` method revert which is problematic for a VRF integration (it is listed in the [VRF Security Considerations docs](https://docs.chain.link/vrf/v2/security#fulfillrandomwords-must-not-revert)).

Another such issue in the method is this code:

```solidity
if (party.assetChainId != getChainId() && address(honeyJarPortal) != address(0) && address(this).balance != 0) {
    uint256 sendAmount = address(this).balance / party.checkpoints.length;
    honeyJarPortal.sendFermentedJars{value: sendAmount}(
        address(this), party.assetChainId, party.bundleId, fermentedJars
    );
}
```

The problem is that when `party.assetChainId != getChainId() && address(honeyJarPortal) != address(0)` are true, then the only thing left to go into the `if` statement is `address(this).balance != 0` - this is easily exploitable as anyone can send 1 wei of ETH into the contract, which will make the expression evaluate to `true`. This will add additional gas cost overhead as it will execute an external call that has more logic, and also the cross-chain call is almost certainly failing as the `sendAmount` is possible to have rounded down to zero (if `address(this).balance` was 1 but `party.checkpoints.length` was more than 1).

**Recommendations**

Consider caching the randomness received and then letting an externally owed account for example to actually make the `_setFermentedJars` call so it can set the correct gas. Also check that the balance is enough to do the `sendFermentedJars` call, not just that the balance is non-zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bearcave |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-BearCave.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

