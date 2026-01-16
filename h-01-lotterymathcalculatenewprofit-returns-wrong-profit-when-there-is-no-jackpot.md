---
# Core Classification
protocol: Wenwin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8902
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-03-wenwin-contest
source_link: https://code4rena.com/reports/2023-03-wenwin
github_link: https://github.com/code-423n4/2023-03-wenwin-findings/issues/324

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - services
  - cross_chain
  - synthetics
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Cyfrin
  - gogo
  - auditor0517
  - bin2chen
  - adriro
---

## Vulnerability Title

[H-01] `LotteryMath.calculateNewProfit` returns wrong profit when there is no jackpot winner

### Overview


This bug report details a vulnerability in the LotteryMath and Lottery contracts on the code-423n4/2023-03-wenwin repository. The function LotteryMath.calculateNewProfit returns the wrong profit when there is no jackpot winner, and the library function is used when we update currentNetProfit of Lottery contract. This can ruin the main functionality of the protocol, as currentNetProfit is used during reward calculation. 

The vulnerability is caused by the incorrect calculation of expectedRewardsOut in LotteryMath.calculateNewProfit when there is no jackpot winner. Instead of multiplying ticketsSold and expectedPayout directly, PercentageMath should be used.

Foundry was the tool used to identify the vulnerability. To mitigate the vulnerability, use PercentageMath instead of multiplying directly in LotteryMath.calculateNewProfit.

### Original Finding Content


<https://github.com/code-423n4/2023-03-wenwin/blob/main/src/LotteryMath.sol#L50-L53>

<https://github.com/code-423n4/2023-03-wenwin/blob/main/src/Lottery.sol#L216-L223>

<https://github.com/code-423n4/2023-03-wenwin/blob/main/src/Lottery.sol#L238-L247>

### Impact

`LotteryMath.calculateNewProfit` returns the wrong profit when there is no jackpot winner, and the library function is used when we update `currentNetProfit` of `Lottery` contract.

```solidity
        currentNetProfit = LotteryMath.calculateNewProfit(
            currentNetProfit,
            ticketsSold[drawFinalized],
            ticketPrice,
            jackpotWinners > 0,
            fixedReward(selectionSize),
            expectedPayout
        );
```

`Lottery.currentNetProfit` is used during reward calculation, so it can ruin the main functionality of this protocol.

```solidity
    function drawRewardSize(uint128 drawId, uint8 winTier) private view returns (uint256 rewardSize) {
        return LotteryMath.calculateReward(
            currentNetProfit,
            fixedReward(winTier), 
            fixedReward(selectionSize),
            ticketsSold[drawId],
            winTier == selectionSize,
            expectedPayout
        );
    }
```

### Proof of Concept

In `LotteryMath.calculateNewProfit`, `expectedRewardsOut` is calculated as follows:

```solidity
        uint256 expectedRewardsOut = jackpotWon
            ? calculateReward(oldProfit, fixedJackpotSize, fixedJackpotSize, ticketsSold, true, expectedPayout)
            : calculateMultiplier(calculateExcessPot(oldProfit, fixedJackpotSize), ticketsSold, expectedPayout)
                * ticketsSold * expectedPayout;
```

The calculation is not correct when there is no jackpot winner. When `jackpotWon` is false, `ticketsSold * expectedPayout` is the total payout in reward token, and then we need to apply a multiplier to the total payout, and the multiplier is `calculateMultiplier(calculateExcessPot(oldProfit, fixedJackpotSize), ticketsSold, expectedPayout)`.

The calculation result is `expectedRewardsOut`, and it is also in reward token, so we should use `PercentageMath` instead of multiplying directly.

For coded PoC, I added this function in `LotteryMath.sol` and imported `forge-std/console.sol` for console log.

```solidity
    function testCalculateNewProfit() public {
        int256 oldProfit = 0;
        uint256 ticketsSold = 1;
        uint256 ticketPrice = 5 ether;
        uint256 fixedJackpotSize = 1_000_000e18; // don't affect the profit when oldProfit is 0, use arbitrary value
        uint256 expectedPayout = 38e16;
        int256 newProfit = LotteryMath.calculateNewProfit(oldProfit, ticketsSold, ticketPrice, false, fixedJackpotSize, expectedPayout );

        uint256 TICKET_PRICE_TO_POT = 70_000;
        uint256 ticketsSalesToPot = PercentageMath.getPercentage(ticketsSold * ticketPrice, TICKET_PRICE_TO_POT);
        int256 expectedProfit = oldProfit + int256(ticketsSalesToPot);
        uint256 expectedRewardsOut = ticketsSold * expectedPayout; // full percent because oldProfit is 0
        expectedProfit -= int256(expectedRewardsOut);
        
        console.log("Calculated value (Decimal 15):");
        console.logInt(newProfit / 1e15); // use decimal 15 for output purpose

        console.log("Expected value (Decimal 15):");
        console.logInt(expectedProfit / 1e15);
    }
```

The result is as follows:

      Calculated value (Decimal 15):
      -37996500
      Expected value (Decimal 15):
      3120

### Tools Used

Foundry

### Recommended Mitigation Steps

Use `PercentageMath` instead of multiplying directly.

```solidity
        uint256 expectedRewardsOut = jackpotWon
            ? calculateReward(oldProfit, fixedJackpotSize, fixedJackpotSize, ticketsSold, true, expectedPayout)
            : (ticketsSold * expectedPayout).getPercentage(
                calculateMultiplier(calculateExcessPot(oldProfit, fixedJackpotSize), ticketsSold, expectedPayout)
            )
```

**[rand0c0des (Wenwin) confirmed](https://github.com/code-423n4/2023-03-wenwin-findings/issues/219)** 

***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Wenwin |
| Report Date | N/A |
| Finders | Cyfrin, gogo, auditor0517, bin2chen, adriro, anodaram, minhtrng, Yukti_Chinta |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-wenwin
- **GitHub**: https://github.com/code-423n4/2023-03-wenwin-findings/issues/324
- **Contest**: https://code4rena.com/contests/2023-03-wenwin-contest

### Keywords for Search

`vulnerability`

