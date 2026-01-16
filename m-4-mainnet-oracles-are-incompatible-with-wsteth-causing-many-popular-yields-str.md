---
# Core Classification
protocol: Blueberry Update #3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24324
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/96

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
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-4: Mainnet oracles are incompatible with wstETH causing many popular yields strategies to be broken

### Overview


This bug report is about incompatibility between mainnet oracles and wstETH, which causes many popular yields strategies to be broken. The ChainlinkAdapterOracle only supports single asset price data, making it incompatible with wstETH, as Chainlink does not have a wstETH oracle on mainnet. Additionally, Band protocol also does not offer a wstETH oracle. This leaves Uniswap oracles as the only option, which is dangerous due to their low liquidity. 

The code snippet provided in the report is from the ChainlinkAdapterOracle.sol file, lines 111-125. The vulnerability detail section provides an explanation of the code. 

The impact of this bug is that many popular yields strategies are broken. 

The tool used to find this bug was manual review. The recommendation given was to create a special bypass for wstETH utilizing the stETH oracle and its current exchange rate.

The discussion section of the report includes comments from two people, 0xPhilic and Kral01, who believed the issue to be of low severity. IAm0x52 then escalated the issue, stating that the protocol is meant to be compatible with these pools but can't work with them, making the issue a valid medium. This was confirmed by Gornutz and Hrishibhat, and the issue was marked as a valid medium.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/96 

## Found by 
0x52

Mainnet oracles are incompatible with wstETH causing many popular yields strategies to be broken. Chainlink and Band do not have wstETH oracles and using Uniswap LP pairs would be very dangerous given their low liquidity. 

## Vulnerability Detail

[ChainlinkAdapterOracle.sol#L111-L125](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/ChainlinkAdapterOracle.sol#L111-L125)

        uint256 decimals = registry.decimals(token, USD);
        (
            uint80 roundID,
            int256 answer,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = registry.latestRoundData(token, USD);
        if (updatedAt < block.timestamp - maxDelayTime)
            revert Errors.PRICE_OUTDATED(token_);
        if (answer <= 0) revert Errors.PRICE_NEGATIVE(token_);
        if (answeredInRound < roundID) revert Errors.PRICE_OUTDATED(token_);

        return
            (answer.toUint256() * Constants.PRICE_PRECISION) / 10 ** decimals;

ChainlinkAdapterOracle only supports single asset price data. This makes it completely incompatible with wstETH because chainlink doesn't have a wstETH oracle on mainnet. Additionally Band protocol doesn't offer a wstETH oracle either. This only leaves Uniswap oracles which are highly dangerous given their low liquidity.

## Impact

Mainnet oracles are incompatible with wstETH causing many popular yields strategies to be broken

## Code Snippet

[ChainlinkAdapterOracle.sol#L102-L126](https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/ChainlinkAdapterOracle.sol#L102-L126)

## Tool used

Manual Review

## Recommendation

Create a special bypass specifically for wstETH utilizing the stETH oracle and it's current exchange rate. 



## Discussion

**sherlock-admin2**

2 comment(s) were left on this issue during the judging contest.

**0xyPhilic** commented:
> invalid because this issue can be considered informational or at best low - tokens used are whitelisted

**Kral01** commented:
> low severity



**IAm0x52**

Escalate

This was wrongly excluded. Protocol is meant to be compatible with these pools but can't work with them. I believe this is a valid medium because the protocol is nonfunctional in this area.

**sherlock-admin2**

 > Escalate
> 
> This was wrongly excluded. Protocol is meant to be compatible with these pools but can't work with them. I believe this is a valid medium because the protocol is nonfunctional in this area.

You've created a valid escalation!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Shogoki**

> Escalate
> 
> This was wrongly excluded. Protocol is meant to be compatible with these pools but can't work with them. I believe this is a valid medium because the protocol is nonfunctional in this area.

Not sure were it says that the protcol is meant to be compatible with `WSTETH` pools on mainnet. 

If that is the case it can be a valid issue, i guess. 
However if it is not, i think the Whitelisting of tokens would count for invalidating it.

**IAm0x52**

Protocol is meant to be compatible with Aura/Convex. wstETH is a component of many highly attractive pools. Not being able to support wstETH as an underlying asset will break support for these.

**hrishibhat**

@Gornutz 

**Gornutz**

Confirm this is valid. 

**hrishibhat**

Result:
Medium
Unique
Considering this issue a valid medium


**sherlock-admin2**

Escalations have been resolved successfully!

Escalation status:
- [IAm0x52](https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/96/#issuecomment-1694747143): accepted

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/96
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`vulnerability`

