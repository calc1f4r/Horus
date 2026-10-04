---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41151
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#1-user-incurs-fee-loss-when-using-burn_unlock_code-with-a-notset-token-status
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

User incurs fee loss when using `BURN_UNLOCK_CODE` with a `NotSet` token status

### Overview


The bug report describes an issue where a user's funds can get stuck when trying to use a specific code to unlock a token. This can happen when the status of the token is changed to "NotSet" by the contract owner. The user may lose their funds if they try to unlock and transfer the token to another chain. The report suggests adding a check in the contract to prevent this from happening.

### Original Finding Content

##### Description

A user's funds may get stuck when using `BURN_UNLOCK_CODE` for a `NotSet` token.

For example, consider the following scenario:
1. A user locks `1000e18` LP tokens on chain A and mints corresponding synthLp tokens on chain B.
2. As time progresses, the `WhitelistV2` contract's owner sets the LP token's status on chain A to `NotSet`.
3. The user decides to unlock their LP tokens and `BURN_UNLOCK_CODE` from chain B to A.
4. While the "burn" operation is successful on chain B, it fails on chain A due to the requirement that the output token must be set as `InOut`:
```solidity
require(
    IWhitelist(whitelist).tokenState(otoken) 
        == uint8(IWhitelist.TokenState.InOut), 
    "Portal: token must be whitelisted");
```
https://github.com/eywa-protocol/eywa-clp/blob/d68ba027ff19e927d64de123b2b02f15a43f8214/contracts/PortalV2.sol#L87

Therefore, the user loses the commission for the cross-chain transaction.

##### Recommendation

We recommend adding a check (similar to the one in the Portal contract) during operations with synthetic tokens in the Synthesis contract to ensure that the token has been added to the whitelist in the 'Whitelist' contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/CLP/README.md#1-user-incurs-fee-loss-when-using-burn_unlock_code-with-a-notset-token-status
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

