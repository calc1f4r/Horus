---
# Core Classification
protocol: Radiant June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36379
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-08] Bypassable `checkLastBlockAction` Modifier

### Overview


The bug report explains that there is a problem with a modifier called `checkLastBlockAction` which is meant to prevent users from depositing and withdrawing from the same block in a smart contract. However, the report states that this check can be easily bypassed, allowing users to still deposit and withdraw in the same block by transferring their shares to another address they control. The severity of this bug is low, but the likelihood of it happening is high. To fix this issue, the report recommends overriding a function called `_afterTokenTransfer` to update a mapping called `_callerLastBlockAction` for the address the tokens are being transferred to. This will ensure that the restriction on block actions applies consistently, even when tokens are transferred between addresses.

### Original Finding Content

**Severity**

**Impact:** Low

**Likelihood:** High

**Description**

The `checkLastBlockAction` modifier is intended to prevent users from depositing and withdrawing in the same block, likely as a measure against flash loan attacks. However, this check can be easily bypassed. A user can deposit and receive share tokens, then transfer these shares to another address they control and proceed to withdraw in the same block from that address.

```solidity
	modifier checkLastBlockAction() {
		if (_callerLastBlockAction[msg.sender] == block.number) revert UniV3TokenizedLp_NoDepositOrWithdrawLoop();
		_;
		_callerLastBlockAction[msg.sender] = block.number;
	}
<...>
	function deposit(
		uint256 deposit0,
		uint256 deposit1,
		address to
	) external override nonReentrant checkLastBlockAction returns (uint256 shares) {
<...>
	function withdraw(
		uint256 shares,
		address to
	) external override nonReentrant checkLastBlockAction returns (uint256 amount0, uint256 amount1) {
```

**Recommendations**

To address this issue, override the `_afterTokenTransfer` function to update the `_callerLastBlockAction` mapping for the `to` address. This ensures that the restriction on block actions applies consistently, even when tokens are transferred between addresses.

```solidity
function _afterTokenTransfer(address from, address to, uint256 amount) internal override {
    super._afterTokenTransfer(from, to, amount);
    _callerLastBlockAction[to] = block.number;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

