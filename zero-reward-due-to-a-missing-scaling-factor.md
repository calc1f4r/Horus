---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36267
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - bladesec
  - RiaZul
  - emmac002
  - pacelli
---

## Vulnerability Title

Zero reward due to a missing scaling factor

### Overview

See description below for full details.

### Original Finding Content

## Summary

When a caller triggers `seasonfacet:gm` or `seasonfacet:sunrise`, according to the comment 'gm advances Beanstalk to the next Season and sends reward Beans to a specified address or the caller'. The calculation of the reward is based on the blocks late and a formula in `LibIncentive:fracExp`, however there is a missing scaling factor (secondsLate <= 240) in fracExp which causes an unintended reduction of incentive to 0.

<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/LibIncentive.sol#L440-L444>

## Vulnerability Details

Step 1: A caller triggers `seasonfacet:gm` and gm returns incentive at the end of the function.
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L61>

```Solidity
    function gm(
        address account,
        LibTransfer.To mode
    ) public payable fundsSafu noOutFlow returns (uint256) {
        require(!s.sys.paused, "Season: Paused.");
        require(seasonTime() > s.sys.season.current, "Season: Still current Season.");
        uint32 season = stepSeason();
        int256 deltaB = stepOracle();
        uint256 caseId = calcCaseIdandUpdate(deltaB);
        LibGerminate.endTotalGermination(season, LibWhitelistedTokens.getWhitelistedTokens());
        LibGauge.stepGauge();
        stepSun(deltaB, caseId);

    @>    return incentivize(account, mode);
    }
```

Step 2: The `LibIncentive:determineReward` calculates the incentive Amount.
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L104>

```Solidity
    function incentivize(address account, LibTransfer.To mode) private returns (uint256) {
        uint256 secondsLate = block.timestamp.sub(
            s.sys.season.start.add(s.sys.season.period.mul(s.sys.season.current))
        );

        // reset USD Token prices and TWA reserves in storage for all whitelisted Well LP Tokens.
        address[] memory whitelistedWells = LibWhitelistedTokens.getWhitelistedWellLpTokens();
        for (uint256 i; i < whitelistedWells.length; i++) {
            LibWell.resetUsdTokenPriceForWell(whitelistedWells[i]);
            LibWell.resetTwaReservesForWell(whitelistedWells[i]);
        }

        @> uint256 incentiveAmount = LibIncentive.determineReward(secondsLate);

        LibTransfer.mintToken(C.bean(), incentiveAmount, account, mode);

        emit LibIncentive.Incentivization(account, incentiveAmount);
        return incentiveAmount;
    }
```

Step 3: The `LibIncentive:determineReward` triggers `LibIncentive:fracExp`, a function which scales the reward up as the number of blocks after expected sunrise increases.
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/LibIncentive.sol#L52>

```Solidity
    function determineReward(uint256 secondsLate) external pure returns (uint256) {
        // Cap the maximum number of blocks late. If the sunrise is later than
        // this, Beanstalk will pay the same amount. Prevents unbounded return value.
        if (secondsLate > MAX_SECONDS_LATE) {
            secondsLate = MAX_SECONDS_LATE;
        }

        // Scale the reward up as the number of blocks after expected sunrise increases.
        // `sunriseReward * (1 + 1/100)^(blocks late * seconds per block)`
        // NOTE: 1.01^(25 * 12) = 19.78, This is the maximum multiplier.
        @> return fracExp(BASE_REWARD, secondsLate);
    }
```

Step 4: The comment in `LibIncentive:fracExp` states that 'Checked every 2 seconds to reduce bytecode size.' However, 240 secondsLate is missing between 238 and 242, which causes an unintended reduction of incentive to 0.
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/LibIncentive.sol#L440-L444>

```Solidity
            if (secondsLate <= 238) {
                return _scaleReward(beans, 10_677_927);
            }
            @audit here
        } else if (secondsLate <= 270) {
            if (secondsLate <= 242) {
                return _scaleReward(beans, 11_111_494);
            }
```

## POC

Test:

```Solidity
    function testfracExp239_240() public {

        uint256 scaledSunriseReward238 = LibIncentive.fracExp(BASE_REWARD, 238);
        uint256 scaledSunriseReward239 = LibIncentive.fracExp(BASE_REWARD, 239);
        uint256 scaledSunriseReward240 = LibIncentive.fracExp(BASE_REWARD, 240);
        uint256 scaledSunriseReward242 = LibIncentive.fracExp(BASE_REWARD, 242);
        uint256 scaledSunriseReward244 = LibIncentive.fracExp(BASE_REWARD, 244);


        console.log("scaledSunriseReward238:", scaledSunriseReward238);
        console.log("scaledSunriseReward239:", scaledSunriseReward239);
        console.log("scaledSunriseReward240:", scaledSunriseReward240);
        console.log("scaledSunriseReward242:", scaledSunriseReward242);
        console.log("scaledSunriseReward244:", scaledSunriseReward244);
    }
```

Result:

```Solidity
Logs:
  scaledSunriseReward238: 53389635
  scaledSunriseReward239: 0
  scaledSunriseReward240: 0
  scaledSunriseReward242: 55557470
  scaledSunriseReward244: 56674175
```

## Impact

The caller or specified address will not receive any reward or 0 reward minted due to a technical flaw, which may lead to a lack of incentives for user participation.

## Tools Used

Manual review & Foundry

## Recommendations

Add secondsLate <= 240

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | bladesec, RiaZul, emmac002, pacelli |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`vulnerability`

