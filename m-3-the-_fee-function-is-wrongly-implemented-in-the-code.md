---
# Core Classification
protocol: Buffer Finance
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3629
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/24
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/95

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 1

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ch\_301
---

## Vulnerability Title

M-3: The `_fee()` function is wrongly implemented in the code

### Overview


This bug report is about an issue found in the code of the Buffer Protocol v2. The issue is with the `_fee()` function which is implemented incorrectly. This leads to the protocol earning fewer fees than expected and the trader earning more. The code snippet included in the report shows how the function is currently implemented. The impact of this bug is that the protocol will earn fewer fees than expected. The bug was found by manual review and the recommendation is to implement the `_fee()` function in this way: `total_fee = (5000 * amount)/ (10000 - sf)`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/95 

## Found by 
Ch\_301

## Summary
 _fee() function is wrongly implemented in the code so the protocol will get fewer fees and the trader will earn more

## Vulnerability Detail
```solidity
        (uint256 unitFee, , ) = _fees(10**decimals(), settlementFeePercentage);
        amount = (newFee * 10**decimals()) / unitFee;
```
let's say we have:
`newFee` 100 USDC
USDC Decimals is 6
`settlementFeePercentage` is 20% ==> 200

The `unitFee` will be 520_000

`amount` = (100 * 1_000_000) / 520_000 
`amount` = 192 USDC
Which is supposed to be  `amount` = 160 USDC

## Impact
The protocol will earn fees less than expected

## Code Snippet
```solidity
       function checkParams(OptionParams calldata optionParams)
        external
        view
        override
        returns (
            uint256 amount,
            uint256 revisedFee,
            bool isReferralValid
        )
    {
        require(
            assetCategory != AssetCategory.Forex ||
                isInCreationWindow(optionParams.period),
            "O30"
        );

        uint256 maxAmount = getMaxUtilization();

        // Calculate the max fee due to the max txn limit
        uint256 maxPerTxnFee = ((pool.availableBalance() *
            config.optionFeePerTxnLimitPercent()) / 100e2);
        uint256 newFee = min(optionParams.totalFee, maxPerTxnFee);

        // Calculate the amount here from the new fees
        uint256 settlementFeePercentage;
        (
            settlementFeePercentage,
            isReferralValid
        ) = _getSettlementFeePercentage(
            referral.codeOwner(optionParams.referralCode),
            optionParams.user,
            _getbaseSettlementFeePercentage(optionParams.isAbove),
            optionParams.traderNFTId
        );
        (uint256 unitFee, , ) = _fees(10**decimals(), settlementFeePercentage);
        amount = (newFee * 10**decimals()) / unitFee;

```
https://github.com/bufferfinance/Buffer-Protocol-v2/blob/83d85d9b18f1a4d09c728adaa0dde4c37406dfed/contracts/core/BufferBinaryOptions.sol#L318-L353

```solidity
    function _fees(uint256 amount, uint256 settlementFeePercentage)
        internal
        pure
        returns (
            uint256 total,
            uint256 settlementFee,
            uint256 premium
        )
    {
        // Probability for ATM options will always be 0.5 due to which we can skip using BSM
        premium = amount / 2;
        settlementFee = (amount * settlementFeePercentage) / 1e4;
        total = settlementFee + premium;
    }

```
https://github.com/bufferfinance/Buffer-Protocol-v2/blob/83d85d9b18f1a4d09c728adaa0dde4c37406dfed/contracts/core/BufferBinaryOptions.sol#L424-L437

## Tool used

Manual Review

## Recommendation
The `_fee()` function needs to calculate the fees in this way
```solidity
total_fee = (5000 * amount)/ (10000 - sf)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Buffer Finance |
| Report Date | N/A |
| Finders | Ch\_301 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/95
- **Contest**: https://app.sherlock.xyz/audits/contests/24

### Keywords for Search

`Wrong Math`

