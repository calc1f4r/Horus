---
# Core Classification
protocol: Govworld
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56267
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-12-02-GovWorld.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Function getRestAmount does not work properly at GOVToken.sol

### Overview


There is an issue with the variable totalAmount in the code. It is being re-initialized every time the loop runs, so it only stores the total amount for the latest type of vesting. This means that the total amount for all vesting types is not being accurately calculated. To fix this, the code should be changed to add the total amount for each vesting type to the existing totalAmount variable. This has been fixed in the code.

### Original Finding Content

**Description**

The variable totalAmount is re-initialized at each iteration of the loop. This means that it
always stores the total amount only for the latest type of vesting.
// Returns the amount of vesting tokens still locked
function getRestAmount(address sender) public view returns (uint256) {
uint256 totalAmount = 0;
for(uint256 i = 0; i < vestingTypes.length; i++){
totalAmount = vestingWallets[i][sender].totalAmount;
}
return totalAmount - getUnlockedVestingAmount(sender);
}

**Recommendation**:

Replace totalAmount =vestingWallets[i][sender].totalAmount; with totalAmount +=
vestingWallets[i][sender].totalAmount;.

**Re-audit**:

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Govworld |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-12-02-GovWorld.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

