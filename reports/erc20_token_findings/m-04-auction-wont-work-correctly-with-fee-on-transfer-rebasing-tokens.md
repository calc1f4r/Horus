---
# Core Classification
protocol: Rolling Dutch Auction
chain: everychain
category: uncategorized
vulnerability_type: auction

# Attack Vector Details
attack_type: auction
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20554
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-Rolling Dutch Auction.md
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
  - auction
  - fee_on_transfer

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-04] Auction won't work correctly with fee-on-transfer & rebasing tokens

### Overview


This bug report describes a problem with the code in the `createAuction` function, which caches the expected transferred amount from the `reserveToken`. This is a problem if the `reserveToken` has a fee-on-transfer mechanism, since the actual received amount will be less due to the fee, or if the token used has a rebasing mechanism, as this can mean that the contract will hold less balance than what it cached in `state.reserves` for the auction, or it will hold more, which will be stuck in the protocol.

The impact is high, as it can lead to a loss of value, and the likelihood is low, as such tokens are not so common.

Recommendations are provided to address the issue. These include documenting that tokens with a fee-on-transfer or rebasing mechanism are not supported, or checking the balance before and after the transfer and using the difference as the actual amount received, or when tokens go down in value, updating the cached `reserves` accordingly based on the balance held, and when they go up in value, adding a method to transfer the excess tokens out of the protocol.

### Original Finding Content

**Impact:**
High, as it can lead to a loss of value

**Likelihood:**
Low, as such tokens are not so common

**Description**

The code in `createAuction` does the following:

```solidity
IERC20(reserveToken).transferFrom(msg.sender, address(this), reserveAmount);
...
...
state.reserves = reserveAmount;
```

so it basically caches the expected transferred amount. This will not work if the `reserveToken` has a fee-on-transfer mechanism, since the actual received amount will be less because of the fee. It is also a problem if the token used had a rebasing mechanism, as this can mean that the contract will hold less balance than what it cached in `state.reserves` for the auction, or it will hold more, which will be stuck in the protocol.

**Recommendations**

You can either explicitly document that you do not support tokens with a fee-on-transfer or rebasing mechanism or you can do the following:

1. For fee-on-transfer tokens, check the balance before and after the transfer and use the difference as the actual amount received.
2. For rebasing tokens, when they go down in value, you should have a method to update the cached `reserves` accordingly, based on the balance held. This is a complex solution.
3. For rebasing tokens, when they go up in value, you should add a method to actually transfer the excess tokens out of the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Rolling Dutch Auction |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-Rolling Dutch Auction.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Auction, Fee On Transfer`

