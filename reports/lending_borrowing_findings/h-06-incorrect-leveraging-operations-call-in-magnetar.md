---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31437
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-06] Incorrect leveraging operations call in Magnetar

### Overview


This bug report discusses an issue with the Magnetar contract, which has functions that interact with the Singularity and BigBang markets. These functions allow users to buy and sell collateral tokens, but the current version of the contracts is using the wrong interface from a previous version, causing them to not work properly. The report recommends changing the function calls to match the current version of the markets in order to fix this issue.

### Original Finding Content

**Severity**

**Impact**: Medium, broken functionality

**Likelihood**: High, broken functionality never works

**Description**

The Magnetar contract has helper functions to interact with the Singularity and BigBang markets which also does multiple compounded operations at the same time for added functionality. One such operation which is supported by the BigBang and Singularity markets is the ability to buy and sell the collateral tokens. This is supported in the BigBang and Singularity markets as shown by the function prototypes below.

```solidity
function buyCollateral(
        address from,
        uint256 borrowAmount,
        uint256 supplyAmount,
        bytes calldata data
    ){...}
function sellCollateral(
        address from,
        uint256 share,
        bytes calldata data
    ){...}
```

The issue is that the Magnetar contracts use the wrong interface from a previous iteration of the protocol which does not work with the current version of the contracts. This evident from the calls seen in the Magnetar contracts.

```solidity
IMarket(_action.target).buyCollateral(
                    from,
                    borrowAmount,
                    supplyAmount,
                    minAmountOut,
                    swapper,
                    dexData
                );

IMarket(_action.target).sellCollateral(
                    from,
                    share,
                    minAmountOut,
                    swapper,
                    dexData
                );
```

As we can see from the function calls, the caller passes in 5 values but the function actually expects only 3 values in its function prototype, thus leading to broken functionality.

There are two instances of this issue in `MagnetarV2.sol`.

- [ ] action.id `MARKET_BUY_COLLATERAL`
- [ ] action.id `MARKET_SELL_COLLATERAL`

**Recommendations**

Change the function calls to conform to the current version of the markets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

