---
# Core Classification
protocol: Beanstalk
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50518
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/beanstalk/beanstalk-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/beanstalk/beanstalk-smart-contract-security-assessment
github_link: none

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

protocol_categories:
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

INTERNAL BALANCE TOKENS CAN BE DRAINED THROUGH THE CURVEFACET.EXCHANGEUNDERLYING FUNCTION

### Overview


The report describes a bug in the CurveFacet contract, specifically in the `exchangeUnderlying()` function. This function is used to swap underlying assets from different Curve stable pools. The bug allows users to swap tokens that belong to other users, resulting in stolen tokens. The bug occurs when a user sets the `fromMode` to `INTERNAL_TOLERANT` and the value returned by the `receiveToken()` call is not checked. This can be abused by users to swap tokens that belong to other users. The report provides details of the pool and underlying tokens involved in the bug, along with the steps to reproduce it. It also includes a screenshot showing the stolen tokens. The bug has been assigned an impact and likelihood score of 5, and the recommendation is to overwrite `amountIn` with the value returned from the `receiveToken()` call to solve the issue. The Beanstalk team has already implemented this solution.

### Original Finding Content

##### Description

In the `CurveFacet`, the `exchangeUnderlying()` function is used to swap underlying assets from different Curve stable pools:

#### CurveFacet.sol

```
function exchangeUnderlying(
    address pool,
    address fromToken,
    address toToken,
    uint256 amountIn,
    uint256 minAmountOut,
    LibTransfer.From fromMode,
    LibTransfer.To toMode
) external payable nonReentrant {
    (int128 i, int128 j) = getUnderlyingIandJ(fromToken, toToken, pool);
    IERC20(fromToken).receiveToken(amountIn, msg.sender, fromMode);
    IERC20(fromToken).approveToken(pool, amountIn);

    if (toMode == LibTransfer.To.EXTERNAL) {
        ICurvePoolR(pool).exchange_underlying(
            i,
            j,
            amountIn,
            minAmountOut,
            msg.sender
        );
    } else {
        uint256 amountOut = ICurvePool(pool).exchange_underlying(
            i,
            j,
            amountIn,
            minAmountOut
        );
        msg.sender.increaseInternalBalance(IERC20(toToken), amountOut);
    }
}

```

\color{black}
\color{white}

The `LibTransfer.From fromMode` has 4 different modes:

* `EXTERNAL`
* `INTERNAL`
* `EXTERNAL_INTERNAL`
* `INTERNAL_TOLERANT`

With the `INTERNAL_TOLERANT` fromMode tokens will be collected from the user's Internal Balance and the transaction will not fail if there is not enough tokens there.

As in the `receiveToken()` call, users can use the `INTERNAL_TOLERANT` fromMode and the value returned by `receiveToken()` is not checked users can abuse this and swap tokens that belong to other users (tokens that are part of other users' internal balance).

Pool: [0x99AE07e7Ab61DCCE4383A86d14F61C68CdCCbf27](https://etherscan.io/address/0x99AE07e7Ab61DCCE4383A86d14F61C68CdCCbf27)
Underlying WBTC: [0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599](https://etherscan.io/address/0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599)
Underlying sBTC: [0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6](https://etherscan.io/address/0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6)

1. User8 transfers `10_000000000000000000` sBTC tokens to his internal balance.
2. User2 calls `exchangeUnderlying()` with an `INTERNAL_TOLERANT` fromMode, setting as the `amountIn` `10_000000000000000000` and as `fromToken` the sBTC token address. These sBTC tokens do belong to user8.
3. User2 successfully swaps for free the sBTC for the WBTC tokens, getting `10_00184757` WBTC in his external balance.
4. Now User8 tries to withdraw from his internal balance the `10_000000000000000000` sBTC tokens he had deposited previously, but the transactions fails as the contract does not have those tokens anymore. They were swapped and stolen by user2.

![4.png](https://halbornmainframe.com/proxy/audits/images/659e8389a1aa3698c0e94dfb)

##### Score

Impact: 5  
Likelihood: 5

##### Recommendation

**SOLVED**: The `Beanstalk team` corrected the issue by overwritting `amountIn` with the value returned from the `receiveToken()` call, as suggested.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Beanstalk |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/beanstalk/beanstalk-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/beanstalk/beanstalk-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

