---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6530
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/176

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel  hyh
  - kenzo
---

## Vulnerability Title

[M-08] SingleNativeTokenExitV2 assumes first exchange holds the outputToken

### Overview


This bug report discusses an issue with the SingleNativeTokenExitV2 contract, which allows users to execute trades via multiple exchanges. The problem is that when the user sends a single output token back to themself, the contract takes that token from the last swap in the first exchange's trades. This impairs the exit functionality, as the user may not be able to exchange the token they desire. 

For example, if a basket holds only token TOKE and the user wants to exchange it for DAI, but there is no exchange with good liquidity for TOKE -> DAI, the user could craft a trade to exchange TOKE for WOKE in exchange A, and then exchange WOKE for DAI in exchange B, to finally receive back DAI. The contract will not let them do this, as the output token is taken to be the output token of the first exchange - WOKE in this example. 

The code reference provided in the report shows that the output token is taken to be the last token exchanged in the first exchange. This manifests the issue detailed in the report.

The recommended mitigation step is to have the outputToken be a parameter supplied in ExitTokenStructV2. This would allow users to receive the desired output token when executing trades via multiple exchanges.

### Original Finding Content


_Submitted by kenzo, also found by cmichel and hyh_

SingleNativeTokenExitV2 allows the user to exit and execute trades via multiple exchanges.
When finishing the trades and sending a single output token back to the user,
the contract takes that token from the last swap in the first exchange's trades.
There is nothing in the struct that signifies this will be the output token, and this also impairs the exit functionality.

#### Impact

Let's say a basket only holds token TOKE, and user would like to exit to DAI.
But there's no exchange with good liquidity for TOKE -> DAI.
So the user crafts a trade to exchange TOKE for WOKE in exchange A, and then exchange WOKE for DAI in exchange B, to finally receive back DAI. The contract will not let him do so, as the output token is taken to be the output token of the first exchange - WOKE in our example.

#### Proof of Concept

In `exit`, the output token is taken to be the last token exchanged in the first exchange: [(Code ref)](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/singleJoinExit/SingleNativeTokenExitV2.sol#L92:#L96)

    address[] calldata path = _exitTokenStruct
                .trades[0]
                .swaps[_exitTokenStruct.trades[0].swaps.length - 1]
                .path;
            IERC20 outputToken = IERC20(path[path.length - 1]); //this could be not the target token

This manifests the issue I detailed above.

#### Recommended Mitigation Steps

Have the outputToken be a parameter supplied in ExitTokenStructV2.

**[loki-sama (Amun) acknowledged](https://github.com/code-423n4/2021-12-amun-findings/issues/176)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | cmichel  hyh, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/176
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

