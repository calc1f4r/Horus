---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3576
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/11
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/109

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
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

M-5: updateTrust() vouchers also need check maxVouchers

### Overview


This bug report is about an issue identified in the code of the Union Finance project. Bin2chen found that the "vouchers" array was not being checked for the maximum number of vouchers, which could potentially cause the updateLocked() function to fail. The code snippet provided shows that the "vouchees" array is checked for the maximum number of vouchers, but the "vouchers" array is not. The recommended solution is to add an additional check for the "vouchers" array to ensure it is not over the maximum number of vouchers.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/109 

## Found by 
bin2chen

## Summary
maxVouchers is to prevent the “vouchees“ array from getting too big and the loop will have the GAS explosion problem, but “vouchers“have the same problem, if you don't check the vouchers array, it is also possible that vouchers are big and cause updateLocked() to fail

## Vulnerability Detail
https://github.com/sherlock-audit/2022-10-union-finance/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L548

vouchees check < maxVouchers ,but vouchers don't check
```
    function updateTrust(address borrower, uint96 trustAmount) external onlyMember(msg.sender) whenNotPaused {
...
            uint256 voucheesLength = vouchees[staker].length;
            if (voucheesLength >= maxVouchers) revert MaxVouchees();


            uint256 voucherIndex = vouchers[borrower].length;
            voucherIndexes[borrower][staker] = Index(true, uint128(voucherIndex));
            vouchers[borrower].push(Vouch(staker, trustAmount, 0, 0)); /**** don't check maxVouchers****/
```
## Impact
 it is also possible that vouchers are big and cause updateLocked() to fail
## Code Snippet

## Tool used

Manual Review

## Recommendation

```solidity

   function updateTrust(address borrower, uint96 trustAmount) external onlyMember(msg.sender) whenNotPaused {
...
            uint256 voucheesLength = vouchees[staker].length;
            if (voucheesLength >= maxVouchers) revert MaxVouchees();


            uint256 voucherIndex = vouchers[borrower].length;
+         if (voucherIndex >= maxVouchers) revert MaxVouchees();
            voucherIndexes[borrower][staker] = Index(true, uint128(voucherIndex));
            vouchers[borrower].push(Vouch(staker, trustAmount, 0, 0)); 

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-union-finance-judging/issues/109
- **Contest**: https://app.sherlock.xyz/audits/contests/11

### Keywords for Search

`vulnerability`

