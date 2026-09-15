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
solodit_id: 16255
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-04-caviar-private-pools
source_link: https://code4rena.com/reports/2023-04-caviar
github_link: https://github.com/code-423n4/2023-04-caviar-findings/issues/463

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
finders_count: 10
finders:
  - JGcarv
  - J4de
  - DishWasher
  - RaymondFam
  - CodingNameKiki
---

## Vulnerability Title

[M-10] Incorrect protocol fee is taken when changing NFTs

### Overview


A bug has been identified in the code for the Caviar protocol which results in an incorrect protocol fee being taken when changing NFTs. This results in a profit loss for the Caviar protocol. The bug is located in the PrivatePool.sol code at line 737. The protocol fee in changeFeeQuote is calculated as a percentage of the feeAmount which is based on the input amount, while in buyQuote and sellQuote the protocol fee is calculated as a percentage of the input amount. To fix the bug, the protocolFeeAmount in changeFeeQuote should be a percentage of the input amount instead of the pool fee. The bug was identified using manual review.

### Original Finding Content


Incorrect protocol fee is taken when changing NFTs which results in profit loss for the Caviar protocol.

### Proof of Concept

The protocol fee in changeFeeQuote is calculated as a percentage of the feeAmount which is based on the input amount:

<https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L737>

```solidity
function changeFeeQuote(uint256 inputAmount) public view returns (uint256 feeAmount, uint256 protocolFeeAmount) {
    ...
    protocolFeeAmount = feeAmount * Factory(factory).protocolFeeRate() / 10_000;
```

This seems wrong as in buyQuote and sellQuote the protocol fee is calculated as a percentage of the input amount, not the pool fee amount:

<https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L703>

```solidity
function buyQuote(uint256 outputAmount)
    ...
    protocolFeeAmount = inputAmount * Factory(factory).protocolFeeRate() / 10_000;
```

<https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L721>

```solidity
function sellQuote(uint256 inputAmount)
    ...
    protocolFeeAmount = outputAmount * Factory(factory).protocolFeeRate() / 10_000;
```

This makes the protocol fee extremely low meaning a profit loss for the protocol.

### Recommended Mitigation Steps

`protocolFeeAmount` in changeFeeQuote should be a percentage of the input amount instead of the pool fee.

**[outdoteth (Caviar) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/463#issuecomment-1518567170):**
 > There is no risk of fund loss here. But agree that this is an issue.

**[outdoteth (Caviar) mitigated](https://github.com/code-423n4/2023-04-caviar-findings/issues/463#issuecomment-1520531536):**
 > Fix is here: https://github.com/outdoteth/caviar-private-pools/pull/13.
> 
> Proposed fix is to add a separate fee called protocolChangeFeeRate which can be much higher than protocolFeeRate. For example, protocolChangeFeeRate could be on the order of ~20-30%. For example, if the fixed `changeFee` is 0.1 ETH, the NFT is worth 1.5 ETH, and the protocolChangeFeeRate is 30%, then the protocol fee would be 0.03 ETH on a change() or flashLoan().
> 
> ```solidity
> function changeFeeQuote(uint256 inputAmount) public view returns (uint256 feeAmount, uint256 protocolFeeAmount) {
>     // multiply the changeFee to get the fee per NFT (4 decimals of accuracy)
>     uint256 exponent = baseToken == address(0) ? 18 - 4 : ERC20(baseToken).decimals() - 4;
>     uint256 feePerNft = changeFee * 10 ** exponent;
> 
>     feeAmount = inputAmount * feePerNft / 1e18;
>     protocolFeeAmount = feeAmount * Factory(factory).protocolChangeFeeRate() / 10_000;
> }
> ```
**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/463#issuecomment-1528971055):**
 > The Warden has shown an inconsistency in how protocolFees are computed, because this is limited to a loss of Yield, I believe Medium Severity to be more appropriate.

**Status:** Mitigation confirmed. Full details in reports from [rbserver](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/23), [KrisApostolov](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/44), and [rvierdiiev](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/13).



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
| Finders | JGcarv, J4de, DishWasher, RaymondFam, CodingNameKiki, Voyvoda, saian, GT_Blockchain, neumo, Josiah |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-caviar
- **GitHub**: https://github.com/code-423n4/2023-04-caviar-findings/issues/463
- **Contest**: https://code4rena.com/contests/2023-04-caviar-private-pools

### Keywords for Search

`vulnerability`

