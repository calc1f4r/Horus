---
# Core Classification
protocol: KlimaDAO Autocompounder
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52436
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/klimadao/klimadao-autocompounder
source_link: https://www.halborn.com/audits/klimadao/klimadao-autocompounder
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Unrestricted deadlines for swaps

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `addLiquidity()` and the `_chargeGreenFee()` functions of the `StrategyAerodromeGaugeGreenFee` contract, there are several interactions with the Aerodrome router that allow for unlimited deadlines.

  

When interacting with external AMM protocols such as Aerodrome, it is recommended to avoid setting the deadline parameter to the current `block.timestamp`.

  

A malicious block builder can withhold swap transactions and execute them later when it's advantageous for manipulating the price or offloading tokens onto the user at a disadvantageous price. Implementing a deadline parameter restricts the time frame during which an attacker can carry out such exploits.

  

#### Code Location

```
function addLiquidity() internal {
    uint256 outputBal = IERC20(output).balanceOf(address(this));
    uint256 lp0Amt = outputBal / 2;
    uint256 lp1Amt = outputBal - lp0Amt;

    if (stable) {
        uint256 lp0Decimals = 10 ** IERC20Extended(lpToken0).decimals();
        uint256 lp1Decimals = 10 ** IERC20Extended(lpToken1).decimals();
        uint256 out0 = lpToken0 != output
            ? (ISolidlyRouter(unirouter).getAmountsOut(lp0Amt, outputToLp0Route)[outputToLp0Route.length] * 1e18) /
                lp0Decimals
            : lp0Amt;
        uint256 out1 = lpToken1 != output
            ? (ISolidlyRouter(unirouter).getAmountsOut(lp1Amt, outputToLp1Route)[outputToLp1Route.length] * 1e18) /
                lp1Decimals
            : lp1Amt;
        (uint256 amountA, uint256 amountB, ) = ISolidlyRouter(unirouter).quoteAddLiquidity(
            lpToken0,
            lpToken1,
            stable,
            factory,
            out0,
            out1
        );
        amountA = (amountA * 1e18) / lp0Decimals;
        amountB = (amountB * 1e18) / lp1Decimals;
        uint256 ratio = (((out0 * 1e18) / out1) * amountB) / amountA;
        lp0Amt = (outputBal * 1e18) / (ratio + 1e18);
        lp1Amt = outputBal - lp0Amt;
    }

    if (lpToken0 != output) {
        ISolidlyRouter(unirouter).swapExactTokensForTokens(
            lp0Amt,
            0,
            outputToLp0Route,
            address(this),
            block.timestamp
        );
    }

    if (lpToken1 != output) {
        ISolidlyRouter(unirouter).swapExactTokensForTokens(
            lp1Amt,
            0,
            outputToLp1Route,
            address(this),
            block.timestamp
        );
    }

    uint256 lp0Bal = IERC20(lpToken0).balanceOf(address(this));
    uint256 lp1Bal = IERC20(lpToken1).balanceOf(address(this));

    ISolidlyRouter(unirouter).addLiquidity(
        lpToken0,
        lpToken1,
        stable,
        lp0Bal,
        lp1Bal,
        1,
        1,
        address(this),
        block.timestamp
    );
}
```

  

```
function _chargeGreenFee() internal returns (uint256 _feeCharged) {
    uint256 outputBal = IERC20(output).balanceOf(address(this));
    (, , uint256 totalFeeInOutputToken) = getPerPoolGreenFee(outputBal);

    if (totalFeeInOutputToken == 0) {
        return 0;
    }

    address greenFeeToken = greenFeeConfig.greenFeeToken;

    uint256 greenFeeTokenBal;
    if (greenFeeToken != output) {  
        // swap output to greenFeeToken
        ISolidlyRouter(unirouter).swapExactTokensForTokens(
            totalFeeInOutputToken,
            0,
            outputToGreenFeeRoute,
            address(this),
            block.timestamp
        );
        greenFeeTokenBal = IERC20(greenFeeToken).balanceOf(address(this));
    } else {
        greenFeeTokenBal = totalFeeInOutputToken;
    }

    // Deposit all green token to green fee vault
    uint256 actualFeeDeposited = _depositGreenFee(greenFeeTokenBal);

    if (actualFeeDeposited != 0) {
        emit ContributedGreenFee(vault, actualFeeDeposited);
    }
}
```

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:U/C:N/A:C/I:C/D:C/Y:C (3.5)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:U/C:N/A:C/I:C/D:C/Y:C)

##### Recommendation

Implement a more robust deadline parameter in order to restrict the time frame during which a trade can be executed.

##### Remediation

**RISK ACCEPTED:** The **KlimaDAO team** made a business decision to accept the risk of this finding and not alter the contracts, stating:

*Code is part of fork.*

##### References

[KlimaDAO/autocompounder/contracts/BIFI/strategies/Aerodrome/StrategyAerodromeGaugeGreen.sol#L186-L251](https://github.com/KlimaDAO/autocompounder/blob/a9ff58ef2bceaac59a13fb2d3ae41b4ae399accf/contracts/BIFI/strategies/Aerodrome/StrategyAerodromeGaugeGreen.sol#L186-L251)

[KlimaDAO/autocompounder/contracts/BIFI/strategies/Aerodrome/StrategyAerodromeGaugeGreen.sol#L170](https://github.com/KlimaDAO/autocompounder/blob/a9ff58ef2bceaac59a13fb2d3ae41b4ae399accf/contracts/BIFI/strategies/Aerodrome/StrategyAerodromeGaugeGreen.sol#L170)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | KlimaDAO Autocompounder |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/klimadao/klimadao-autocompounder
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/klimadao/klimadao-autocompounder

### Keywords for Search

`vulnerability`

