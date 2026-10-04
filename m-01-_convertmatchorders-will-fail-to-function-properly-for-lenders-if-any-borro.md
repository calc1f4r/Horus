---
# Core Classification
protocol: Stusdcxbloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55681
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
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
  - @IAm0x52
---

## Vulnerability Title

[M-01] \_convertMatchOrders will fail to function properly for lenders if any borrower has canceled a matched order

### Overview


The bug report describes an issue in a function called "killBorrowerMatch" in a code called BloomPool. This function is used to cancel a transaction between a lender and a borrower. The problem occurs when a borrower cancels the transaction and all the values inside the transaction are set to zero, causing the matching process to break prematurely. This leads to a potential for malicious borrowers to disrupt the matching process and cause inconvenience to both lenders and borrowers. The recommendation is to fix this issue by popping empty matches and continuing with the matching process. This issue has been fixed in a recent update.

### Original Finding Content

**Details**

    function killBorrowerMatch(address lender) external returns (uint256 lenderAmount, uint256 borrowerReturn) {
        MatchOrder[] storage matches = _userMatchedOrders[lender];

        uint256 len = matches.length;
        for (uint256 i = 0; i != len; ++i) {
            if (matches[i].borrower == msg.sender) {
                lenderAmount = uint256(matches[i].lCollateral);
                borrowerReturn = uint256(matches[i].bCollateral);
                // Zero out the match order to preserve the array's order
                matches[i] = MatchOrder({lCollateral: 0, bCollateral: 0, borrower: address(0)});
                // Decrement the matched depth and open move the lenders collateral to an open order.
                _matchedDepth -= lenderAmount;
                _openOrder(lender, lenderAmount);
                break;
            }
        }

When a borrower kills a match, all values are zeroed out inside the MatchOrder struct and it is kept in the lender's matches array. This leads to a problem later when trying to match the lenders orders.

[BloomPool.sol#L382-L415](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L382-L415)

    uint256 length = matches.length;
    for (uint256 i = length; i != 0; --i) {
        uint256 index = i - 1;


        if (remainingAmount != 0) {
            (uint256 lenderFunds, uint256 borrowerFunds) =
                _calculateRemovalAmounts(remainingAmount, matches[index].lCollateral, matches[index].bCollateral);
            uint256 amountToRemove = lenderFunds + borrowerFunds;

            if (amountToRemove == 0) break; <- @audit matching loop breaks when collateral in match is 0
            remainingAmount -= amountToRemove;

            _borrowerAmounts[matches[index].borrower][id] += borrowerFunds;
            borrowerAmountConverted += borrowerFunds;

            emit MatchOrderConverted(id, account, matches[index].borrower, lenderFunds, borrowerFunds);

            if (lenderFunds == matches[index].lCollateral) {
                matches.pop();
            } else {
                matches[index].lCollateral -= uint128(lenderFunds);
            }
        } else {
            break;
        }
    }

We see above that when the collateral is 0 as it is with a canceled match, the matching loop breaks prematurely. Given this is FILO matching, all deposits made prior the cancelled order will be impossible to match. Those borrowers will need to all manually cancel their orders and resubmit. This presents a high potential for griefing as a malicious borrower can DOS lenders and borrowers alike.

**Lines of Code**

[BloomPool.sol#L377-L416](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L377-L416)

**Recommendation**

BloomPool#\_convertMatchOrders should pop empty matches and continue rather than breaking.

**Remediation**

Fixed as recommended in bloom-v2 [PR#15](https://github.com/Blueberryfi/bloom-v2/pull/15)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Stusdcxbloom |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

