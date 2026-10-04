---
# Core Classification
protocol: Teller Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32383
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/70

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
  - 0x3b
  - 0xadrii
---

## Vulnerability Title

M-6: Utilization math should include `liquidityThresholdPercent`

### Overview


This bug report highlights an issue with the Teller Finance protocol where the utilization math does not include the `liquidityThresholdPercent` variable. This variable represents the maximum amount that can be borrowed, and not including it in the calculation can result in misleading APRs and lower profits for LPs. The impact of this bug is a breakdown of the core contract functionality, as utilization above the threshold is unreachable. The recommendation is to include the `liquidityThresholdPercent` variable in the calculation. The protocol team has already fixed this issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/70 

## Found by 
0x3b, 0xadrii
## Summary
Utilization math should include `liquidityThresholdPercent`, as this represents the maximum value that can be borrowed. This means that if borrowing reaches `principal * liquidityThresholdPercent`, then 100% of the available assets are considered borrowed.

## Vulnerability Detail
[getPoolUtilizationRatio](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L757) is used within [getMinInterestRate](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L769) to calculate the interest rate at which borrowers borrow. Higher utilization equates to a higher APR.

However, in the current case, [getMinInterestRate](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L769) fails to include `liquidityThresholdPercent` in its calculation. This variable is crucial as it caps the maximum borrowing allowed (e.g., if it's 80%, then a maximum of 80% of the assets can be borrowed).

Not including this variable means that the utilization (and thus the APR) will appear lower than it actually is. An example of this is a more risky market with a lower `liquidityThresholdPercent`, such as 40%. In these markets, even though there is some risk that the LPs take, the maximum utilization will be 40%, as borrowers cannot borrow above that, even if there is demand for this token. This in tern will decease the profits LPs make from staking in risky markets.

## Impact
This results in a breakdown of core contract functionality. Utilization above `liquidityThresholdPercent` is unreachable, leading to lower LP profits.

## Code Snippet
```solidity
    function getPoolUtilizationRatio() public view returns (uint16) {
        if (getPoolTotalEstimatedValue() == 0) { return 0; }

        return uint16( Math.min(
           getTotalPrincipalTokensOutstandingInActiveLoans() * 10000 / 
           getPoolTotalEstimatedValue(), 10000 ));
    }   
```
## Tool used
Manual Review

## Recommendation
Include `liquidityThresholdPercent` in [getPoolUtilizationRatio](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L757). For example:

```diff
-   return uint16(Math.min(getTotalPrincipalTokensOutstandingInActiveLoans() * 10000 / getPoolTotalEstimatedValue(), 10000));
+   return uint16(Math.min(getTotalPrincipalTokensOutstandingInActiveLoans() * 10000 / (getPoolTotalEstimatedValue().percent(liquidityThresholdPercent)), 10000));
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/17

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | 0x3b, 0xadrii |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/70
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

