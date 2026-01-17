---
# Core Classification
protocol: Genius Contracts Re-Assessment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51975
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
source_link: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
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

Centralization Risks in Protocol's Access Control Design

### Overview

See description below for full details.

### Original Finding Content

##### Description

The protocol implementation grants excessive privileges to administrative roles, enabling fund extraction through multiple vectors. This centralization manifests in three critical functions across the protocol's contracts:

  

1. In **GeniusVaultCore.sol**, the `fillOrder` function allows unrestricted execution by orchestrators:

   ```
   function fillOrder(
       Order memory order,
       address swapTarget,
       bytes memory swapData,
       address callTarget,
       bytes memory callData
   ) external virtual override nonReentrant onlyOrchestrator whenNotPaused {
      // No limit on fund movement through swap operations
   ```
2. In **GeniusVaultCore.sol**, `rebalanceLiquidity` provides access to substantial fund movement:

   ```
   function rebalanceLiquidity(
       uint256 amountIn,
       uint256 dstChainId,
       address target,
       bytes calldata data
   ) external payable virtual override onlyOrchestrator whenNotPaused {
       if (target == address(0)) revert GeniusErrors.NonAddress0();
       _isAmountValid(amountIn, availableAssets());
       // Can drain up to rebalanceThreshold
   ```
3. In **GeniusMultiTokenVault.sol**, `swapToStables` enables orchestrator-controlled token drainage:

   ```
   function swapToStables(
       address token,
       uint256 amount,
       address target,
       bytes calldata data
   ) external override onlyOrchestrator whenNotPaused {
      // Can drain non-stablecoin tokens by manipulating output validation
   ```
4. In **GeniusVault.sol**, `withdrawFunds` :

   ```
   function withdrawFunds() external onlyAdmin {
           uint256 balance = STABLECOIN.balanceOf(address(this));
           STABLECOIN.safeTransfer(msg.sender, balance);
       }
   ```

  

**Impact:**

1. The admin/orchestrator roles possess unilateral control over user funds
2. No time-locks or multi-signature requirements protect high-risk operations
3. A single compromised admin account can lead to complete protocol drainage
4. Users must place complete trust in the protocol administrators

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to add value limits for sensitive operations done by admins, implement multi-signature requirements.

##### Remediation

**ACKNOWLEDGED:** The **Shuttle Labs team** acknowledge the issue and will switch to a governance as soon as possible.

##### References

[Shuttle-Labs/genius-contracts/src/GeniusVaultCore.sol#L193](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusVaultCore.sol#L193)

[Shuttle-Labs/genius-contracts/src/GeniusVaultCore.sol#L120](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusVaultCore.sol#L120)

[Shuttle-Labs/genius-contracts/src/GeniusMultiTokenVault.sol#L135](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusMultiTokenVault.sol#L135)

[Shuttle-Labs/genius-contracts/src/GeniusVault.sol#L140](https://github.com/Shuttle-Labs/genius-contracts/blob/main/src/GeniusVault.sol#L140)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genius Contracts Re-Assessment |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/shuttle-labs/genius-contracts-re-assessment

### Keywords for Search

`vulnerability`

