---
# Core Classification
protocol: Caviar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16251
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-04-caviar-private-pools
source_link: https://code4rena.com/reports/2023-04-caviar
github_link: https://github.com/code-423n4/2023-04-caviar-findings/issues/697

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
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

[M-06] Flashloan fee is not distributed to the factory

### Overview


This bug report is about an issue with the PrivatePool.sol code on the 2023-04-caviar repository on Github. When a user takes a flashloan, he pays a fee to the PrivatePool, but the whole fee amount is sent to the PrivatePool, and the factory receives nothing. Other functions of the contract, such as the 'change' function, calculate pool and protocol fees, but in the case of flashloan, only the pool receives the fees. The bug was discovered using VsCode.

The recommended mitigation step to solve this issue is to send some part of the flashloan fee to the factory.

### Original Finding Content


When user takes a flashloan, then [he pays a fee](https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L651) to the PrivatePool.
The problem is that the whole fee amount is sent to PrivatePool and factory receives nothing.

However, all other function of contract send some part of fees to the factory.

For example, `change` function, which is similar to the `flashloan` as it doesn't change virtual nft and balance reserves. This function [calculates pool and protocol fees](https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L736-L737).

But in case of flashloan, only pool receives fees.

### Tools Used

VS Code

### Recommended Mitigation Steps

Send some part of flashloan fee to the factory.

**[outdoteth (Caviar) confirmed and commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/697#issuecomment-1519957289):**
 > Fixed in: https://github.com/outdoteth/caviar-private-pools/pull/8.
> 
> Proposed fix is to add a method that returns the protocol fee and flash fee. And then have the flash fee function sum the two outputs:
> 
> ```solidity
> function flashFeeAndProtocolFee() public view returns (uint256 feeAmount, uint256 protocolFeeAmount) {
>     // multiply the changeFee to get the fee per NFT (4 decimals of accuracy)
>     uint256 exponent = baseToken == address(0) ? 18 - 4 : ERC20(baseToken).decimals() - 4;
>     feeAmount = changeFee * 10 ** exponent;
>     protocolFeeAmount = feeAmount * Factory(factory).protocolFeeRate() / 10_000;
> }
> 
> 
> function flashFee(address, uint256) public view returns (uint256) {
>     (uint256 feeAmount, uint256 protocolFeeAmount) = flashFeeAndProtocolFee();
>     return feeAmount + protocolFeeAmount;
> }
> ```
> 
> and then add the protocol payment in the flashLoan method:
> 
> ```solidity
> // -- snip -- //
> 
> if (baseToken != address(0)) {
>     // transfer the fee from the borrower
>     ERC20(baseToken).safeTransferFrom(msg.sender, address(this), flashFee);
> 
>     // transfer the protocol fee to the factory
>     ERC20(baseToken).safeTransferFrom(msg.sender, factory, protocolFee);
> } else {
>     // transfer the protocol fee to the factory
>     factory.safeTransferETH(protocolFee);
> }
> ```

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/697#issuecomment-1528972275):**
 > @outdoteth - Can you please confirm if you originally intended to have the protocol charge a fee for Flashloans?

**[outdoteth (Caviar) commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/697#issuecomment-1530128568):**
 > It was an oversight that we did not charge fees on flash loans. It's implied that it should be paid though since protocol fees are charged everywhere else a user makes a transaction.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/697#issuecomment-1531011905):**
 > The Warden has found an inconsistency as to how fees are paid. After confirming with the Sponsor, I agree with Medium Severity.

**Status:** Mitigation confirmed. Full details in reports from [rbserver](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/31), [KrisApostolov](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/41), and [rvierdiiev](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/11).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-caviar
- **GitHub**: https://github.com/code-423n4/2023-04-caviar-findings/issues/697
- **Contest**: https://code4rena.com/contests/2023-04-caviar-private-pools

### Keywords for Search

`vulnerability`

