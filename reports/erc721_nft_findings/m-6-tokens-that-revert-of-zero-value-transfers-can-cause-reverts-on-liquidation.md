---
# Core Classification
protocol: Teller Lender Groups Update Audit
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44221
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/51

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
  - liquidation
  - revert_on_0_transfer

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hash
---

## Vulnerability Title

M-6: Tokens that revert of zero value transfers can cause reverts on liquidation

### Overview


The report discusses an issue with tokens that cause reverts on liquidation. The root cause is that the code does not check if the token value is zero before transferring it. This can lead to incorrect values for shares during liquidation. The report recommends checking for non-zero values before transferring tokens to mitigate the issue. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/51 

## Found by 
hash
### Summary

Tokens that revert of zero value transfers can cause reverts on liquidation

### Root Cause

In the [readme the team has mentioned](https://github.com/sherlock-audit/2024-11-teller-finance-update/tree/main?tab=readme-ov-file#q-if-you-are-integrating-tokens-are-you-allowing-only-whitelisted-tokens-to-work-with-the-codebase-or-any-complying-with-the-standard-are-they-assumed-to-have-certain-properties-eg-be-non-reentrant-are-there-any-types-of-weird-tokens-you-want-to-integrate) that they would like to know if any wierd token breaks their contract pools

In multiple places token amount which can become zero is transferred without checking the value is zero. This will cause these transactions to revert
https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L699-L727
```solidity
            IERC20(principalToken).safeTransferFrom(
                msg.sender,
                address(this),
                amountDue + tokensToTakeFromSender - liquidationProtocolFee
            ); 
             
            address protocolFeeRecipient = ITellerV2(address(TELLER_V2)).getProtocolFeeRecipient();


              IERC20(principalToken).safeTransferFrom(
                msg.sender,
                address(protocolFeeRecipient),
                 liquidationProtocolFee
            );


            totalPrincipalTokensRepaid += amountDue;
            tokenDifferenceFromLiquidations += int256(tokensToTakeFromSender - liquidationProtocolFee );

        } else {

            uint256 tokensToGiveToSender = abs(minAmountDifference);


           
            IERC20(principalToken).safeTransferFrom(
                msg.sender,
                address(this),
                amountDue - tokensToGiveToSender  
            );
```

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

In case liquidation reverts (due to tokensToGiveToSender == -amountDue), the `tokenDifferenceFromLiquidations` won't be updated which will cause the value of the shares to be incorrectly high (because in reality the auction is settling at 0 price) 

### PoC

_No response_

### Mitigation

Check if amount is non-zero before transferring

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | hash |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`Liquidation, Revert On 0 Transfer`

