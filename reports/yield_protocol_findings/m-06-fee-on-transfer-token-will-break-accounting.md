---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58110
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
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

[M-06] Fee on Transfer Token Will Break accounting

### Overview


This bug report highlights an issue with the `mint()` and `deposit()` functions in the `As4626.sol` file. These functions use the `amount` parameter for transferring and accounting, but this could cause problems with fee on transfer tokens. This is because the actual token received may be less than the amount specified, leading to incorrect accounting and affecting the `sharePrice`. While the likelihood of this bug occurring is low, the impact is high as it could result in incorrect accounting. The report recommends using before and after balance checks to accurately reflect the true amount received and update the share price accordingly. 

### Original Finding Content

## Severity

**Impact:** High, because the accounting will be incorrect, and the sharePrice will be affected

**Likelihood:** Low, because fee on transfer token is not commonly used

## Description

`mint()/deposit()` is using `amount` for transfering and accounting. But fee on transfer token could break the accounting, since the actual token received will be less than amount. As a result, `sharePrice` will have some small error each time.

```solidity
File: src\abstract\As4626.sol
69:     function mint(
70:         uint256 _shares,
71:         address _receiver
72:     ) public returns (uint256 assets) {
73:         return _deposit(previewMint(_shares), _shares, _receiver);
74:     }

117:     function deposit(
118:         uint256 _amount,
119:         address _receiver
120:     ) public whenNotPaused returns (uint256 shares) {
121:         return _deposit(_amount, previewDeposit(_amount), _receiver);
122:     }

84:     function _deposit(
85:         uint256 _amount,
86:         uint256 _shares,
87:         address _receiver
88:     ) internal nonReentrant returns (uint256) {

98:         asset.safeTransferFrom(msg.sender, address(this), _amount);

105:         _mint(_receiver, _shares);

```

USDT potentially could turn on fee on transfer feature, but not yet.

## Recommendations

Use before and after balance to accurately reflect the true amount received, and update share price accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

