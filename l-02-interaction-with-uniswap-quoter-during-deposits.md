---
# Core Classification
protocol: Aegis-September
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41323
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Aegis-security-review-September.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-02] Interaction with uniswap quoter during deposits

### Overview

See description below for full details.

### Original Finding Content

AegisVaultCore.sol interacts with uniswap quoter contract. It is used during deposits to calculate how much a user would get if they swapped on the targetVault.

```solidity
import { IQuoter } from "@uniswap/v3-periphery/contracts/interfaces/IQuoter.sol";
```

```solidity
    function __deposit(
//...
                // figure out how much token0 the user would get if they were to the swap on the targetVault
                uint256 realDeltaOut0 = _quoter.quoteExactInputSingle(
                    token1, token0, targetVault.fee(), ctx.userDepositAmount1.sub(ctx.userContributionToTotal1), 0
                );
//...
                // figure out how much token1 the user would get if they were to the swap on the targetVault
                uint256 realDeltaOut1 = _quoter.quoteExactInputSingle(
                    token0, token1, targetVault.fee(), ctx.userDepositAmount0.sub(ctx.userContributionToTotal0), 0
                );
  //...
```

However, Uniswap Quoter can be gas-intensive and is not designed to be used onchain, as it's not very stable which can cause unexpected reversions. It is actually recommended for use in the backend by uniswap. From the [docs](https://docs.uniswap.org/contracts/v3/reference/periphery/lens/Quoter)

> Allows getting the expected amount out or amount in for a given swap without executing the swap

> These functions are not gas efficient and should not be called on chain. Instead, optimistically execute the swap and check the amounts in the callback.

Considering how complex the `deposit` function is, introducing such an unstable external call that can be gas intensive can quickly lead to unexpected reverts, reaching the gas limit, and potentially dossing deposits for users.

To fix this might require a slight redesign.

For instance, using an oracle for token valuations and/or using the output of the real swaps instead of quoting the expected amount as recommended by uniswap.

## Aegis team comments

We acknowledge the concerns regarding the gas-intensive nature of Uniswap Quoter interactions during deposits. To mitigate this, we implemented and tested a QuoterView contract, which can be utilized on chains where gas costs are a primary concern. However, in most cases, including Berachain, we will continue to use the standard Uniswap V3 Quoter deployed by the underlying AMM.

Moreover, we have introduced the doCheckImpliedSlippage boolean, which allows bypassing the Quoter entirely in scenarios where all Aegis depositors are known, further optimizing efficiency.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Aegis-September |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Aegis-security-review-September.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

