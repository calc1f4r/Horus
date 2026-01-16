---
# Core Classification
protocol: JOJO Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18476
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/70
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/373

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
  - lending

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - 0xStalin
  - Bauer
  - 0x52
  - cccz
  - Nyx
---

## Vulnerability Title

M-9: FlashLoanLiquidate.JOJOFlashLoan has no slippage control when swapping USDC

### Overview


This bug report is about FlashLoanLiquidate.JOJOFlashLoan, a part of the JOJO exchange. The issue is that this function has no slippage control when swapping USDC, which could expose users to sandwich attacks. The bug was found by 0x52, 0xStalin, Aymen0909, Bauer, Nyx, T1MOH, cccz, peakbolt, and rvierdiiev. They used manual review for their investigation. 

The code snippet provided shows that GeneralRepay.repayJUSD and FlashLoanRepay.JOJOFlashLoan both use the user-supplied minReceive parameter for slippage control when swapping USDC. However, FlashLoanLiquidate.JOJOFlashLoan does not, which is the issue. 

The impact of this bug is that users may be exposed to sandwich attacks when swapping USDC. JoscelynFarr then provided a link to the fix, which was confirmed by IAm0x52. The fix was to make FlashLoanLiquidate.JOJOFlashLoan use the minReceive parameter for slippage control when swapping USDC.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/373 

## Found by 
0x52, 0xStalin, Aymen0909, Bauer, Nyx, T1MOH, cccz, peakbolt, rvierdiiev
## Summary
FlashLoanLiquidate.JOJOFlashLoan has no slippage control when swapping USDC
## Vulnerability Detail
In both GeneralRepay.repayJUSD and FlashLoanRepay.JOJOFlashLoan, the user-supplied minReceive parameter is used for slippage control when swapping USDC. 
```solidity
    function JOJOFlashLoan(
        address asset,
        uint256 amount,
        address to,
        bytes calldata param
    ) external {
        (address approveTarget, address swapTarget, uint256 minReceive, bytes memory data) = abi
            .decode(param, (address, address, uint256, bytes));
        IERC20(asset).approve(approveTarget, amount);
        (bool success, ) = swapTarget.call(data);
        if (success == false) {
            assembly {
                let ptr := mload(0x40)
                let size := returndatasize()
                returndatacopy(ptr, 0, size)
                revert(ptr, size)
            }
        }
        uint256 USDCAmount = IERC20(USDC).balanceOf(address(this));
        require(USDCAmount >= minReceive, "receive amount is too small");
...
    function repayJUSD(
        address asset,
        uint256 amount,
        address to,
        bytes memory param
    ) external {
        IERC20(asset).safeTransferFrom(msg.sender, address(this), amount);
        uint256 minReceive;
        if (asset != USDC) {
            (address approveTarget, address swapTarget, uint256 minAmount, bytes memory data) = abi
                .decode(param, (address, address, uint256, bytes));
            IERC20(asset).approve(approveTarget, amount);
            (bool success, ) = swapTarget.call(data);
            if (success == false) {
                assembly {
                    let ptr := mload(0x40)
                    let size := returndatasize()
                    returndatacopy(ptr, 0, size)
                    revert(ptr, size)
                }
            }
            minReceive = minAmount;
        }

        uint256 USDCAmount = IERC20(USDC).balanceOf(address(this));
        require(USDCAmount >= minReceive, "receive amount is too small");
```
However, this is not done in FlashLoanLiquidate.JOJOFlashLoan, and the lack of slippage control may expose the user to sandwich attacks when swapping USDC.
## Impact
The lack of slippage control may expose the user to sandwich attacks when swapping USDC.
## Code Snippet
https://github.com/sherlock-audit/2023-04-jojo/blob/main/JUSDV1/src/Impl/flashloanImpl/FlashLoanLiquidate.sol#L46-L78

## Tool used

Manual Review

## Recommendation
Consider making FlashLoanLiquidate.JOJOFlashLoan use the minReceive parameter for slippage control when swapping USDC.



## Discussion

**JoscelynFarr**

fix link: https://github.com/JOJOexchange/JUSDV1/commit/b0e7d27cf484d9406a267a1b38ac253113101e8e

**IAm0x52**

Fix looks good. JOJOFlashloan now validates minReceived when swapping

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | JOJO Exchange |
| Report Date | N/A |
| Finders | 0xStalin, Bauer, 0x52, cccz, Nyx, peakbolt, T1MOH, Aymen0909, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-jojo-judging/issues/373
- **Contest**: https://app.sherlock.xyz/audits/contests/70

### Keywords for Search

`vulnerability`

