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
solodit_id: 32369
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/46

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
finders_count: 18
finders:
  - samuraii77
  - y4y
  - kennedy1030
  - bughuntoor
  - pkqs90
---

## Vulnerability Title

H-4: liquidateDefaultedLoanWithIncentive sends the collateral to the wrong account

### Overview


The liquidateDefaultedLoanWithIncentive function in the Teller Finance protocol sends the collateral to the wrong account, which means that liquidators will not be properly incentivized to liquidate. This also leads to incorrect accounting within the LenderCommitmentGroup. The issue was found by multiple individuals and could potentially cause losses for LPs. The vulnerability was found through a manual review and the recommendation is to ensure that the funds are sent to the correct recipient. The Teller Finance team has fixed the issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/46 

## Found by 
0x3b, 0x73696d616f, 0xAnmol, 0xDjango, AuditorPraise, EgisSecurity, KupiaSec, Timenov, blockchain555, bughuntoor, cryptic, jovi, kennedy1030, merlin, no, pkqs90, samuraii77, y4y
## Summary
[liquidateDefaultedLoanWithIncentive](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L422) sends the collateral to the Lender - LenderCommitmentGroup (LCG) instead of the liquidator. Liquidators will not be incentivized to liquidate.

## Vulnerability Detail
[liquidateDefaultedLoanWithIncentive](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L422) is intended to liquidate bids, where liquidators pay off the debt and receive the collateral. However, currently the collateral is sent to the lender - LCG, because [lenderCloseLoanWithRecipient](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L738-L774) includes `msg.sender` as its second parameter but does not utilize it:

```solidity
    function lenderCloseLoanWithRecipient(uint256 _bidId, address _collateralRecipient) external {
        _lenderCloseLoanWithRecipient(_bidId, _collateralRecipient);
    }

    function _lenderCloseLoanWithRecipient(uint256 _bidId, address _collateralRecipient) internal acceptedLoan(_bidId, "lenderClaimCollateral") {
        require(isLoanDefaulted(_bidId), "Loan must be defaulted.");

        Bid storage bid = bids[_bidId];
        bid.state = BidState.CLOSED;

        address sender = _msgSenderForMarket(bid.marketplaceId);
        require(sender == bid.lender, "Only lender can close loan");

        //@audit we directly call `lenderClaimCollateral`
        collateralManager.lenderClaimCollateral(_bidId);
    }
```
[lenderClaimCollateral](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/CollateralManager.sol#L271-L283) in its place withdraws the collateral directly to the lender - LCG, without updating `totalPrincipalTokensRepaid`. Some effects:

- Liquidators will gain 0 profits, so they will not liquidate.
- LPs suffer losses as liquidations are not carried out, and returned collateral from liquidations is not accrued as `totalPrincipalTokensRepaid`, increasing utilization, eventually bricking the contract.

## Impact
Liquidators will not be incentivized to liquidate and incorrect accounting occurs inside LCG.

## Code Snippet
```solidity
    function _lenderCloseLoanWithRecipient(
        uint256 _bidId,
        address _collateralRecipient // @audit never used
    ) internal acceptedLoan(_bidId, "lenderClaimCollateral") {
        require(isLoanDefaulted(_bidId), "Loan must be defaulted.");

        Bid storage bid = bids[_bidId];
        bid.state = BidState.CLOSED;

        address sender = _msgSenderForMarket(bid.marketplaceId);
        require(sender == bid.lender, "Only lender can close loan");

        collateralManager.lenderClaimCollateral(_bidId);
    }
```
## Tool used
Manual Review

## Recommendation
Ensure [_lenderCloseLoanWithRecipient](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/TellerV2.sol#L745-L755) sends the funds to `_collateralRecipient`.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/16/files

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | samuraii77, y4y, kennedy1030, bughuntoor, pkqs90, AuditorPraise, KupiaSec, 0xDjango, blockchain555, no, 0x73696d616f, jovi, 0x3b, EgisSecurity, Timenov, cryptic, merlin, 0xAnmol |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/46
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

