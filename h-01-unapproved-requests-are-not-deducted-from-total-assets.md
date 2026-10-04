---
# Core Classification
protocol: Blueberry_2025-03-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61454
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Unapproved requests are not deducted from total assets

### Overview


The bug report discusses a problem with the `requestRedeem()` function in the `HyperEvmVault` contract. This function does not subtract the requested assets and shares from the total assets and total supply, leading to incorrect share price calculations. This bug has a medium impact and a high likelihood of occurring. The report suggests that the requested amounts should be subtracted from the total assets and total supply when a redemption request is made to fix this issue.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description
In the `HyperEvmVault` contract, the `requestRedeem()` function records the requested assets and shares but does not subtract these amounts from the total assets (`tvl()`) and total supply (`totalSupply()`). This leads to incorrect share price calculations until the withdrawal is finalized.
```solidity
function requestRedeem(uint256 shares_) external nonReentrant {
        V1Storage storage $ = _getV1Storage();
        uint256 balance = this.balanceOf(msg.sender);
        // Determine if the user withdrawal request is valid
        require(shares_ <= balance, Errors.INSUFFICIENT_BALANCE());

        RedeemRequest storage request = $.redeemRequests[msg.sender];
        request.shares += shares_;
        require(request.shares <= balance, Errors.INSUFFICIENT_BALANCE());

        // User will redeem assets at the current share price
        uint256 tvl_ = _totalEscrowValue($);
        _takeFee($, tvl_);
        uint256 assetsToRedeem = shares_.mulDivDown(tvl_, totalSupply());

        request.assets += uint64(assetsToRedeem);
        $.totalRedeemRequests += uint64(assetsToRedeem);
        --snip--
    }
```

**Example:**
Here’s a comparison of the two scenarios (with and without adjusting totals):

1. **Initial State**:  
   - Without Adjusting Totals: The total value locked (TVL) is 1,000,010 assets, and the total supply is 1,000,010 shares.  
   - With Adjusting Totals: The TVL is 1,000,010 assets, and the total supply is 1,000,010 shares.  

2. **User Requests Redemption**:  
   - Without Adjusting Totals: A user requests to redeem 1,000,000 shares and 1,000,000 assets.  
   - With Adjusting Totals: A user requests to redeem 1,000,000 shares and 1,000,000 assets.  

3. **After Request**:  
   - Without Adjusting Totals: The TVL and total supply remain unchanged at 1,000,010 assets and 1,000,010 shares, respectively.  
   - With Adjusting Totals: The TVL is adjusted to 10 assets, and the total supply is adjusted to 10 shares.  

4. **Vault Loses 5 Assets**:  
   - Without Adjusting Totals: The TVL decreases to 1,000,005 assets, while the total supply remains at 1,000,010 shares.  
   - With Adjusting Totals: The TVL decreases to 5 assets, and the total supply remains at 10 shares.  

5. **Share Price Calculation**:  
   - Without Adjusting Totals: The share price is calculated as approximately 1 (1,000,005 / 1,000,010).  
   - With Adjusting Totals: The share price is calculated as 0.5 (5 / 10).  

6. **Impact on Other Users**:  
   - Without Adjusting Totals: Other users can deposit or withdraw at an incorrect share price (~1).  
   - With Adjusting Totals: Other users can deposit or withdraw at the correct share price (0.5).

## Recommendations
Subtract the requested redemption amounts from the total assets (`tvl()`) and total supply when a redemption request is made.





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-03-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

