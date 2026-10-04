---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1858
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backed-protocol-contest
source_link: https://code4rena.com/reports/2022-04-backed
github_link: https://github.com/code-423n4/2022-04-backed-findings/issues/83

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
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - hake
  - minhquanym
  - jah
  - Dravee
  - WatchPug
---

## Vulnerability Title

[M-03] `sendCollateralTo` is unchecked in `closeLoan()`, which can cause user's collateral NFT to be frozen

### Overview


This bug report is about a vulnerability in the code of a smart contract which was written to facilitate NFT loan transactions. The vulnerability occurs when the `sendCollateralTo` is a contract address that does not support ERC721. In this case, the collateral NFT can be frozen in the contract, which could result in an unexpected loss of funds. According to the Ethereum Improvement Proposal (EIP) 721, wallets, brokers, and auction applications must implement the wallet interface if they accept safe transfers. To fix the vulnerability, the code should be changed to use the `safeTransferFrom` function instead of the `transferFrom` function. This will ensure that the collateral NFT is safely transferred to the `sendCollateralTo` address.

### Original Finding Content

_Submitted by WatchPug, also found by berndartmueller, Dravee, hake, jah, and minhquanym_

[NFTLoanFacilitator.sol#L116-L126](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L116-L126)<br>

```solidity
function closeLoan(uint256 loanId, address sendCollateralTo) external override notClosed(loanId) {
    require(IERC721(borrowTicketContract).ownerOf(loanId) == msg.sender,
    "NFTLoanFacilitator: borrow ticket holder only");

    Loan storage loan = loanInfo[loanId];
    require(loan.lastAccumulatedTimestamp == 0, "NFTLoanFacilitator: has lender, use repayAndCloseLoan");
    
    loan.closed = true;
    IERC721(loan.collateralContractAddress).transferFrom(address(this), sendCollateralTo, loan.collateralTokenId);
    emit Close(loanId);
}
```

The `sendCollateralTo` will receive the collateral NFT when `closeLoan()` is called. However, if `sendCollateralTo` is a contract address that does not support ERC721, the collateral NFT can be frozen in the contract.

As per the documentation of EIP-721:

> A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.

Ref: [EIP-721](https://eips.ethereum.org/EIPS/eip-721)

### Recommended Mitigation Steps

Change to:

```solidity
function closeLoan(uint256 loanId, address sendCollateralTo) external override notClosed(loanId) {
    require(IERC721(borrowTicketContract).ownerOf(loanId) == msg.sender,
    "NFTLoanFacilitator: borrow ticket holder only");

    Loan storage loan = loanInfo[loanId];
    require(loan.lastAccumulatedTimestamp == 0, "NFTLoanFacilitator: has lender, use repayAndCloseLoan");
    
    loan.closed = true;
    IERC721(loan.collateralContractAddress).safeTransferFrom(address(this), sendCollateralTo, loan.collateralTokenId);
    emit Close(loanId);
}
```

**[wilsoncusack (Backed Protocol) acknowledged, but disagreed with Medium severity and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/83#issuecomment-1092314347):**
> We use transferFrom and _mint instead of the safe versions to save gas. We think it is a reasonable expectation that users calling this should know what they are doing. We feel this is OK especially because other major protocols like Uniswap do this ([Uniswap/NonfungiblePositionManager.sol#L156](https://github.com/Uniswap/v3-periphery/blob/main/contracts/NonfungiblePositionManager.sol#L156)).

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/83#issuecomment-1100090670):**
 > I believe Med Risk is a fair assessment given the mixed/inconsistent usage of `safeTransferFrom` and `transferFrom` in the contract.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | hake, minhquanym, jah, Dravee, WatchPug, berndartmueller |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backed
- **GitHub**: https://github.com/code-423n4/2022-04-backed-findings/issues/83
- **Contest**: https://code4rena.com/contests/2022-04-backed-protocol-contest

### Keywords for Search

`vulnerability`

