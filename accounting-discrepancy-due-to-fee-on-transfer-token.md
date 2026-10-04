---
# Core Classification
protocol: Yollo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37194
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-10-Yollo.md
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

Accounting discrepancy due to fee-on-transfer token

### Overview


This bug report is about a problem with a cryptocurrency contract called YolloToken. The contract has a feature where users can transfer tokens to another contract called YolloStaking using a special function. However, there is a bug in the code that deducts a fee from the transferred amount, resulting in the user receiving less tokens than expected. This causes an inconsistency in the contract's records and can lead to problems with its accounting. The report suggests adjusting the code to fix this issue.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

The YolloToken contract extends the basic functionality of ERC20 with additional features, such as fee deduction on transfers, and implements the ERC1363 standard. To purchase a package, a user needs to transfer the staking token to the YolloStaking contract using the transferAndCall function. This function enhances the basic token transfer functionality of ERC20. It allows for the transfer of a chosen amount of tokens to a recipient, followed by a callback to the recipient's contract. This process triggers the onTransferReceived hook, executing any relevant logic. However, the overridden _update function deducts a fee from this amount, leading to the actual number of tokens received by the user being less than the specified amount. This results in an accounting discrepancy, where the contract records a higher number of tokens as staked than what the user has actually received post-fee deduction. Such an inconsistency can lead to the breaking of the contract's accounting logic.

**PoC**:
```solidity
      
   function test_onTransferReceivedConsiderTokenFeeWhenUpdatingStakingTokenTransfersForUsers()
       public
   {
       uint256 stakingContractBalanceBefore = yollloToken.balanceOf(
           address(staker)
       );
       vm.startPrank(user1);


       yollloToken.transferAndCall(address(staker), stakeAmount);


       uint256 stakingContractBalanceAfter = yollloToken.balanceOf(
           address(staker)
       );


       assertEq(
           staker.stakingTokenTransfers(user1),
           stakingContractBalanceAfter - stakingContractBalanceBefore
       );
   }
```

  




**Recommendation**: 

Adjust the `onTransferReceived` function to ensure that the recorded staked amount equals the actual amount received.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Yollo |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-10-Yollo.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

