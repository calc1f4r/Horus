---
# Core Classification
protocol: Taurus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7360
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/45
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-taurus-judging/issues/149

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - duc
  - 8olidity
  - y1cunhui
  - cducrest-brainbot
  - Ruhum
---

## Vulnerability Title

M-2: Mint limit is not reduced when the Vault is burning TAU

### Overview


This bug report is about the incorrect updating of `currentMinted` when the Vault is acting on behalf of users when burning TAU. This is because when the burn of `TAU` is performed, it calls `_decreaseCurrentMinted` to reduce the limit of tokens minted by the Vault. It subtracts `accountMinted` (which is `currentMinted[account]`) from `currentMinted[msg.sender]`. When the vault is burning tokens on behalf of the user, the `account` != `msg.sender` meaning the `currentMinted[account]` is 0, and thus the `currentMinted` of Vault will be reduced by 0 making it pretty useless. This issue was found by SunSec, GimelSec, chaduke, shaka, tvdung94, Ruhum, cducrest-brainbot, nobody2018, Chinmay, duc, LethL, y1cunhui, mstpr-brainbot, HonorLt, 8olidity, and bytes032.

The impact of this bug is that `currentMinted` is incorrectly decreased upon burning so vaults do not get more space to mint new tokens. The code snippet related to this bug is available at https://github.com/sherlock-audit/2023-03-taurus/blob/main/taurus-contracts/contracts/TAU.sol#L76-L83. This bug was found using Manual Review. A simple solution would be to change the code snippet to `uint256 accountMinted = currentMinted[msg.sender]` but it is recommended to revisit and rethink the function altogether. The discussion regarding this bug can be found at https://github.com/protokol/taurus-contracts/pull/85.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-taurus-judging/issues/149 

## Found by 
SunSec, GimelSec, chaduke, shaka, tvdung94, Ruhum, cducrest-brainbot, nobody2018, Chinmay, duc, LethL, y1cunhui, mstpr-brainbot, HonorLt, 8olidity, bytes032

## Summary

Upon burning TAU, it incorrectly updates the `currentMinted` when Vault is acting on behalf of users.

## Vulnerability Detail

When the burn of `TAU` is performed, it calls `_decreaseCurrentMinted` to reduce the limit of tokens minted by the Vault:
```solidity
    function _decreaseCurrentMinted(address account, uint256 amount) internal virtual {
        // If the burner is a vault, subtract burnt TAU from its currentMinted.
        // This has a few highly unimportant edge cases which can generally be rectified by increasing the relevant vault's mintLimit.
        uint256 accountMinted = currentMinted[account];
        if (accountMinted >= amount) {
            currentMinted[msg.sender] = accountMinted - amount;
        }
    }
```

The issue is that it subtracts `accountMinted` (which is `currentMinted[account]`) from `currentMinted[msg.sender]`. When the vault is burning tokens on behalf of the user, the `account` != `msg.sender` meaning the `currentMinted[account]` is 0, and thus the `currentMinted` of Vault will be reduced by 0 making it pretty useless.

Another issue is that users can transfer their `TAU` between accounts, and then `amount > accountMinted` will not be triggered.

## Impact

`currentMinted` is incorrectly decreased upon burning so vaults do not get more space to mint new tokens.

## Code Snippet

https://github.com/sherlock-audit/2023-03-taurus/blob/main/taurus-contracts/contracts/TAU.sol#L76-L83

## Tool used

Manual Review

## Recommendation
A simple solution would be to:
```solidity
     uint256 accountMinted = currentMinted[msg.sender];
```
But I suggest revisiting and rethinking this function altogether.

## Discussion

**Sierraescape**

https://github.com/protokol/taurus-contracts/pull/85

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Taurus |
| Report Date | N/A |
| Finders | duc, 8olidity, y1cunhui, cducrest-brainbot, Ruhum, SunSec, shaka, nobody2018, chaduke, bytes032, tvdung94, LethL, HonorLt, mstpr-brainbot, GimelSec, Chinmay |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-taurus-judging/issues/149
- **Contest**: https://app.sherlock.xyz/audits/contests/45

### Keywords for Search

`vulnerability`

