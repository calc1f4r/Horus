---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45528
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1056

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
finders_count: 11
finders:
  - futureHack
  - 0x23r0
  - DenTonylifer
  - Galturok
  - LordAlive
---

## Vulnerability Title

M-38: `liquidationType2` will self DOS due to lack of ETH

### Overview


The issue is that the `liquidationType2` function is not able to access the necessary ETH from the treasury contract, causing it to fail. This means that the liquidation process is not working properly and could potentially lead to a denial of service (DOS) attack. To fix this, the ETH needs to be moved from the treasury to the BorrowLiquidation contract.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1056 

## Found by 
0x23r0, 0x37, DenTonylifer, Galturok, John44, LordAlive, ParthMandale, futureHack, nuthan2x, santiellena, valuevalk

### Summary


ETH is not pulled from the treasury to turn into sUSD. 
Although it's in a payable function, the ETH is inside the treasury contract and admin doesn't have access directly to take ETH out and send via `msg.value`, it has to be pulled internally from treasury when calling liquidation


### Root Cause


lack of ETH movement from treasury into borrowLiquidation contract. So, [borrowLiquidation.liquidationType2](https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L340-L354) will fail.



### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path


When liquidating type 2, the Eth in value is turned into WETH, and then ot is turned into sETH from synthetix.
Then the sETH is turned into sUSD and this amount is used to liquidate.

But the issue is `liquidationType2` on `BorrowLiqudiation` contract lacks the ETH in it. Although its in a payable function, the ETH is inside the treasury contract and admin doesn't have access directly to take ETH out and send via `msg.value`, it has to be pulled from treasury and continue the steps to swap into `sUSD`.

[borrowLiquidation.liquidationType2](https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L340-L354)
```solidity

    function liquidationType2(
        address user,
        uint64 index,
        uint64 currentEthPrice
    ) internal {

//////////////////////////////////////
/////////////////////////////////////
        uint256 amount = BorrowLib.calculateHalfValue(depositDetail.depositedAmountInETH);
        // Convert the ETH into WETH
    @>  weth.deposit{value: amount}();
        // Approve it, to mint sETH
        bool approved = weth.approve(address(wrapper), amount);
        if (!approved) revert BorrowLiq_ApproveFailed();

        // Mint sETH
        wrapper.mint(amount);
        // Exchange sETH with sUSD
        synthetix.exchange(
            0x7345544800000000000000000000000000000000000000000000000000000000,
            amount,
            0x7355534400000000000000000000000000000000000000000000000000000000
        );

        // Calculate the margin
        int256 margin = int256((amount * currentEthPrice) / 100);
        // Transfer the margin to synthetix
        synthetixPerpsV2.transferMargin(margin);

        // Submit an offchain delayed order in synthetix for short position with 1X leverage
        synthetixPerpsV2.submitOffchainDelayedOrder(
            -int((uint(margin * 1 ether * 1e16) / currentEthPrice)),
            currentEthPrice * 1e16
        );
    }
```

### Impact


`liquidationType2` is DOS, broken functionality



### PoC

_No response_

### Mitigation


move ETH from the treasury to BorrowLiquidation

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | futureHack, 0x23r0, DenTonylifer, Galturok, LordAlive, nuthan2x, santiellena, 0x37, ParthMale, valuevalk, John44 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1056
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

