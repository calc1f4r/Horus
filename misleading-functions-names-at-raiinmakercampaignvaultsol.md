---
# Core Classification
protocol: Raiinmaker
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56163
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-05-Raiinmaker.md
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
  - Zokyo
---

## Vulnerability Title

Misleading functions names at RaiinmakerCampaignVault.sol

### Overview


The bug report is about two functions, setFeeAmount() and setFeeAddress(), which are used to assign a fee address and fee amount. The report mentions that there is a missing check for a zero address in setFeeAmount() and recommends changing the functions' names and adding an additional check for the fee address. The recommended code is also provided.

### Original Finding Content

**Description**


Function setFeeAmount() takes as a parameter address and assigns it to the variable
feeAddress. Also in function missed check for zero address.
Function setFeeAddress takes as a parameter uint256 _fee and assigns it to the variable fee.

**Recommendation**:

Change functions names and add an additional checks:
function setFeeAddress(address _address) external onlyMultiSig {
require(_address != address(0), "Wrong fee address");
feeAddress = _address;
emit FeeAddressChanged(_address);
}
function setFeeAmount(uint256 _fee) external onlyMultiSig {
fee = _fee;
emit FeeAmountChanged(_fee);

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Raiinmaker |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-10-05-Raiinmaker.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

