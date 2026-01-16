---
# Core Classification
protocol: DODO Cross-Chain DEX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58590
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/991
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-dodo-cross-chain-dex-judging/issues/856

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
finders_count: 14
finders:
  - hy
  - Ob
  - roadToWatsonN101
  - 0xEkko
  - ZeroTrust
---

## Vulnerability Title

M-8: False “pool exists” detection via `balanceOf()` leads to broken swap paths

### Overview


This bug report discusses an issue with the `_existsPairPool()` function in the `GatewayCrossChain.sol` and `GatewayTransferNative.sol` contracts in the Dodo Cross-Chain DEX. This function uses `ERC20.balanceOf()` to check for the existence of a pool on the UniswapV2 platform, but this can lead to false positives since any address can hold tokens, even without a deployed pair contract. This can cause downstream transaction reverts and denial of service. The root cause is that the function does not verify if the pool has deployed contract code or read real reserves. This can be exploited by an attacker who transfers small amounts of tokens to the computed pair address, causing legitimate swaps to fail and disrupting the user experience. The report suggests a mitigation, but there has been no response from the team. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-05-dodo-cross-chain-dex-judging/issues/856 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
0xEkko, 1337, AnomX, Cybrid, EgisSecurity, Ob, ZeroTrust, hy, mahdiRostami, peppef, roadToWatsonN101, rsam\_eth, silver\_eth, the\_haritz

### Summary

The function `_existsPairPool()` in `GatewayCrossChain.sol` and `GatewayTransferNative.sol` uses `ERC20.balanceOf()` at a computed UniswapV2 pair address to infer pool existence. Because any address can hold tokens—even without a deployed pair contract—this check produces false positives. Consequently, `getPathForTokens()` may return a direct token–token path that does not actually exist, triggering downstream transaction reverts and denial of service.

### Root Cause

In both contracts, `_existsPairPool()` is implemented as follows: https://github.com/sherlock-audit/2025-05-dodo-cross-chain-dex/blob/main/omni-chain-contracts/contracts/GatewayCrossChain.sol#L207-L220

This logic never verifies that `pool` has deployed contract code, nor does it read real reserves via `getReserves()`. It thus treats any stray token balances at that address as liquidity.

### Internal Pre-conditions

1. A call to `getPathForTokens(tokenA, tokenB)` is made.

2. `_existsPairPool()` returns `true` because the computed address holds non-zero balances of both tokens.

3. The actual UniswapV2 pair contract was never deployed at that address.



### External Pre-conditions

1. An EOA or arbitrary contract receives `tokenA` and `tokenB` transfers at the computed pool address.

2. The true UniswapV2 factory has not created a pair for `(tokenA, tokenB)`.

### Attack Path

1. Attacker transfers small amounts of `tokenA` and `tokenB` to the computed pair address (no contract deployed).

2. User or protocol calls `getPathForTokens(tokenA, tokenB)`.

3.` _existsPairPool()` returns `true` (false positive).

4. `getPathForTokens()` returns `[tokenA, tokenB]` instead of fallback path.

5. Downstream swap via UniswapV2 router (e.g., `swapExactTokensForTokens`) attempts to interact with a non-existent pool contract.

6. Transaction reverts, causing denial of service.

### Impact

1. Denial of Service: Legitimate swaps between `tokenA` and `tokenB` cannot execute.

2. Broken UX: Cross-chain transfers or swaps fail unexpectedly whenever a fake “liquidity” address is used.



### PoC

_No response_

### Mitigation

_No response_



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO Cross-Chain DEX |
| Report Date | N/A |
| Finders | hy, Ob, roadToWatsonN101, 0xEkko, ZeroTrust, 1337, Cybrid, mahdiRostami, EgisSecurity, rsam\_eth, silver\_eth, peppef, the\_haritz, AnomX |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-dodo-cross-chain-dex-judging/issues/856
- **Contest**: https://app.sherlock.xyz/audits/contests/991

### Keywords for Search

`vulnerability`

