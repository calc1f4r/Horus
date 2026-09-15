---
# Core Classification
protocol: Elektrik
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37555
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
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

Facilitators can borrow assets and never repay it back

### Overview


The bug report states that there is a potential issue with the borrowing mechanism in the AdvancedOrderEngine smart contract. The documentation mentions that a Facilitator can borrow assets from the vault, but there is no check in place to ensure that these assets are repaid. This could lead to losses within the system. The recommendation is to add a check to validate the repayment of borrowed assets. The client has defended this as a design choice, stating that facilitators are incentivized for their service and cannot borrow assets without repaying them. The auditors have accepted this explanation. 

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Description**

It is mentioned in the documentation that a `Facilitator` has the capability to borrow assets from the `vault`. However, upon reviewing the `AdvancedOrderEngine` smart contract, no mechanism for verifying whether the borrowed assets have been repaid by the Facilitator is observed.
Without proper checks in place, there is a high possibility of assets being borrowed without repayment, leading to potential loss within the system.

**File**: AdvancedOrderEngine.sol

```solidity
701:     function _processFacilitatorInteraction(
702:         bytes calldata facilitatorInteraction,
703:         OrderEngine.Order[] calldata orders,
704:         uint256[] calldata executedSellAmounts,
705:         uint256[] calldata executedBuyAmounts,
706:         ERC20[] calldata borrowedTokens,
707:         uint256[] calldata borrowedAmounts
708:     ) private {
..
724:             // Transfer funds to the 'interactionTarget' address.
725:             for (uint256 i; i < borrowedTokens.length; ) {
726:                 _sendAsset(
727:                     borrowedTokens[i],
728:                     borrowedAmounts[i],
729:                     interactionTarget
730:                 );
731:                 unchecked {
732:                     ++i;
733:                 }
734:             }

```

**Recommendation**: 

Add a check to validate that the borrowed assets have been repaid by the Facilitator.

**Client comment**: 

**Defense Reason**: Design Choice.
**DEFENSE**: Consider the following example



User1
User2
User3
SELL
10 USDC
11 USDC
0.0096 ETH
BUY
0.0048 ETH
0.0048 ETH
20 USDC


In this situation, User3's order will satisfy both User1’s and User2’s orders. Here’s how it works:
- User3 sells 0.0096 ETH, which fulfills User1’s and User2’s requests to buy 0.0048 ETH each.
- In this chain trade, there will be 1 extra USDC token left.

Why does the facilitator get an incentive?

- **Facilitator Incentive**: Facilitators (bots) are rewarded with the extra token for their service. This incentive mechanism ensures that anyone can create these bots, whitelist them, and start matching orders in our distributed architecture.
- **No Unpaid Borrowing**: Facilitators cannot borrow assets without repaying. Users will always receive their specified buy amount. Any extra token is an incentive for the facilitator's service.
- **Comparison with CoW Swap**: On platforms like CoW Swap, solvers (facilitators) can keep the extra token, but there is an additional layer. If the solver willingly foregoes the extra token, their match is accepted, and they are awarded CoW tokens as an incentive.





**Auditors comment**: We have reviewed the explanation provided by the client and accept that this is the intended design choice.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Elektrik |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-09-Elektrik.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

