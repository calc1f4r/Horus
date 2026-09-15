---
# Core Classification
protocol: USDi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55386
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/04/usdi/
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
finders_count: 2
finders:
  - George Kobakhidze
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Validation for BPS Values in Fee Tiers ✓ Fixed

### Overview


The bug report discusses an issue with the `addFeeTier` and `updateFeeTier` functions in the `USDiCoin.sol` contract. These functions allow setting fees without enforcing upper bounds, which can lead to accidental or malicious misconfiguration. This could result in fees being set too high, causing user deposits and withdrawals to fail. The report recommends implementing validation checks to ensure fees remain within a safe range to protect users from potential errors or misuse. 

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

In the `1ae396b8da0f15367703764e3071e8cdffd926a5` commit for fix review the finding has been fixed.

#### Description

The `addFeeTier` and `updateFeeTier` functions allow setting `mintFee` and `burnFee` without enforcing upper bounds. Since these fees are expressed in basis points (BPS), omitting such validation may lead to accidental or malicious misconfiguration. For example, an admin could set the fee to 100% (10,000 BPS), confiscating the entire user deposit or withdrawal. Worse, if a fee is set above 100%, all deposits and withdrawals would revert due to underflow, effectively halting user interactions with the protocol.

#### Examples

**contracts/USDiCoin.sol:L213-L228**

```
/// @notice Adds a new fee tier to the schedule (admin only)
function addFeeTier(uint256 min, uint256 max, uint256 mintFee, uint256 burnFee)
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
{
    feeTiers.push(FeeTier(min, max, mintFee, burnFee));
}

/// @notice Updates an existing fee tier by index (admin only)
function updateFeeTier(uint256 index, uint256 min, uint256 max, uint256 mintFee, uint256 burnFee)
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
{
    require(index < feeTiers.length, "Invalid index");
    feeTiers[index] = FeeTier(min, max, mintFee, burnFee);
}

```

#### Recommendation

We recommend implementing validation checks to ensure that `mintFee` and `burnFee` remain within a safe and reasonable range. For example, to cap fees at 5%, enforce the following:

```
require(mintFee <= 500 && burnFee <= 500, "Fee exceeds maximum allowed");

```

This ensures fee logic remains consistent and protects users from configuration errors or misuse.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | USDi |
| Report Date | N/A |
| Finders | George Kobakhidze,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/04/usdi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

