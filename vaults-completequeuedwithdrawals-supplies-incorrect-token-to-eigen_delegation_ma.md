---
# Core Classification
protocol: Puffer Institutional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50016
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
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
finders_count: 3
finders:
  - Hyh
  - Ladboy233
  - Noah Marconi
---

## Vulnerability Title

Vault's completeQueuedWithdrawals() supplies incorrect token to EIGEN_DELEGATION_MANAGER.completeQueuedWithdrawals()

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low Risk  
**Context:** InstitutionalVault.sol#L312  

## Description
Having the deposit contract address, `IERC20(address(BEACON_DEPOSIT_CONTRACT))`, as a preferred output token, `tokens[0][0]`, isn't correct as this value has to specify the output token to receive, which is not represented by the deposit contract. For now, the tokens value looks to be ignored for the beacon chain case:

- **DelegationManager.sol#L595-L605:**
  ```
  if (receiveAsTokens) {
      // Withdraws `shares` in `strategy` to `withdrawer`. If the shares are virtual beaconChainETH
      shares,,
      ! // then a call is ultimately forwarded to the `staker`s EigenPod; 
      otherwise a call is ultimately forwarded, !
      // to the `strategy` with info on the `token`.
      shareManager.withdrawSharesAsTokens({
          staker: withdrawal.staker,
          strategy: withdrawal.strategies[i],
          token: tokens[i], // <<<
          shares: sharesToWithdraw
      });
  } else {
  ```

- **EigenPodManager.sol#L183-L188:**
  ```
  function withdrawSharesAsTokens(
      address staker,
      IStrategy strategy,
      IERC20, // <<<
      uint256 shares
  ) external onlyDelegationManager nonReentrant {
  ```

However, this might change in the future Eigen Layer versions, which can lead to permanent unavailability of the `completeQueuedWithdrawals()` (while restaked withdrawals can still be completed via `customExternalCall()`).

## Recommendation
Consider using `address(0)` to represent ETH, e.g.:
- `tokens[0][0] = IERC20(address(BEACON_DEPOSIT_CONTRACT));`
- `tokens[0][0] = IERC20(address(0));`

**Puffer Finance:** The address here is wrong, but it shouldn't be `address(0)`, it should be `_BEACON_CHAIN_STRATEGY`. Here is a mainnet tx as an example: [Mainnet Transaction](https://etherscan.io/tx/0xb2a297fbfa18b1dc02548842df36b129ad085a06f57c9b07cee06ff7a70f6ab5)

**Fixed in PR 6.**  
**Cantina Managed:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Puffer Institutional |
| Report Date | N/A |
| Finders | Hyh, Ladboy233, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Puffer-Spearbit-Security-Review-February-2025.pdf

### Keywords for Search

`vulnerability`

