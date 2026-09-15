---
# Core Classification
protocol: Conic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29920
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#10-lptoken-taint-griefing
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
  - MixBytes
---

## Vulnerability Title

LpToken taint griefing

### Overview


The LpToken contract has a bug where users are unable to mint or burn tokens if they have received a large amount of tokens from another user. This can be exploited by malicious actors to block operations of users with large balances or MEV bots. It also prevents users from buying and burning tokens in a single transaction. The recommended solution is to allow users to burn tokens received before the current taint, but not more than that amount.

### Original Finding Content

##### Description

The [LpToken](https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/LpToken.sol) cannot be minted or burned by a user if someone has transferred an amount of LpToken to them greater than `controller.getMinimumTaintedTransferAmount(token)`:
```
function _ensureSingleEvent(address ubo, uint256 amount) internal {
    if(
        !controller.isAllowedMultipleDepositsWithdraws(ubo) &&
        amount > controller.getMinimumTaintedTransferAmount(address(this))
    ) {
        require(
            _lastEvent[ubo] != block.number,
            "cannot mint/burn twice in a block");
        ...
```
https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/LpToken.sol#L81

This means a malicious actor could send a minimum number of tokens to any "whale" (a user with a large balance) trying to make a large deposit or withdraw, thereby blocking their operation. 

For example, this could be used to attack users who want to urgently burn their LP tokens to repay an overcollateralized debt and avoid liquidation. This can also be used to block MEV bots that utilize mint or burn lp tokens in their path strategies. It also removes the ability to buy LP tokens on an exchange and burn them in a single transaction.

It's worth noting that by default, `controller.getMinimumTaintedTransferAmount(token)` equals zero, so the attacker would only need to pay for the gas to block a specific user's operations.

##### Recommendation

We recommended allowing users to burn LP tokens received before the current taint.

For instance, if in the first block a user mints 1000 tokens for themselves, and then in the second block they receive another token, it would be desirable in the second block to still allow them to burn the initial 1000 tokens. However, it should revert if they try to burn more than that amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Conic Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#10-lptoken-taint-griefing
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

