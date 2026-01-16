---
# Core Classification
protocol: CryptoLegacy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61292
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/CryptoLegacy/CryptoLegacy/README.md#5-incorrect-lastbalance-update-in-treasury-token-transfer-for-rebasing-tokens
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

Incorrect `lastBalance` update in treasury token transfer for rebasing tokens

### Overview


The bug report is about a problem in the `LibCryptoLegacy` library's `_transferTreasuryTokensToLegacy` function. The issue is that the `td.lastBalance` variable is being updated incorrectly, which leads to incorrect handling of negative rebases. This can result in the incorrect distribution of tokens to beneficiaries. The severity of this bug is classified as medium because it can cause problems with token distribution. The recommendation is to revert the `lastBalance` update to the previous implementation to prevent this issue from happening.

### Original Finding Content

##### Description
In the `LibCryptoLegacy` library’s `_transferTreasuryTokensToLegacy` function, `td.lastBalance` is updated by adding the difference between the post-transfer balance and the prior balance. This logic miscalculates `lastBalance` under rebasing tokens, leading to incorrect negative rebase handling.
For example, assume after the previous claim `td.lastBalance` is 1,000. A positive rebase increases the contract’s token balance to 1,100. Then, a treasury transfer of 1,000 tokens raises the balance to 2,100. The code sets `td.lastBalance = 1000 + (2100 – 1100) = 2000` instead of the actual 2,100. If a subsequent 0.5% negative rebase reduces the actual balance to 2,089.5, the stale `td.lastBalance` (2,000) is below the new balance, causing `_tokenPrepareToDistribute` to detect a negative rebase and incorrectly increase the recorded `totalClaimed`, reducing future claimable amounts for beneficiaries. 

This misallocation violates vesting invariants when rebasing tokens are involved, warranting **Medium** severity because it corrupts distribution without enabling direct asset theft.
<br/>
##### Recommendation

We recommend reverting the `lastBalance` update to the previous implementation:

```diff
-    td.lastBalance += IERC20(_tokens[i]).balanceOf(address(this)) 
-                      - balanceBefore;
+    td.lastBalance = IERC20(_tokens[i]).balanceOf(address(this));
```

This change ensures `lastBalance` always matches the actual post-transfer balance and prevents erroneous claim adjustments caused by rebasing.


---


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | CryptoLegacy |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/CryptoLegacy/CryptoLegacy/README.md#5-incorrect-lastbalance-update-in-treasury-token-transfer-for-rebasing-tokens
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

