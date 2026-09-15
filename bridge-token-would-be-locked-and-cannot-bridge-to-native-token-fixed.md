---
# Core Classification
protocol: Linea Canonical Token Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26794
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/06/linea-canonical-token-bridge/
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
finders_count: 2
finders:
  -  Tejaswa Rastogi

  - Rai Yang
---

## Vulnerability Title

Bridge Token Would Be Locked and Cannot Bridge to Native Token ✓ Fixed

### Overview


This bug report is regarding the Linea team's pull request [66](https://github.com/Consensys/linea-token-bridge/pull/66) and its final commit hash as `8f8ee32cf3ad24ec669b62910d3d6eb1da9cc78e`. The bug occurs when a bridge token B of a native token A is already deployed and `confirmDeployment` is called on the other layer and `setDeployed` sets A’s `nativeToBridgedToken` value to `DEPLOYED_STATUS`. The bridge token B cannot bridge to native token A in `completeBridging` function, because A’s `nativeToBridgedToken` value is not `NATIVE_STATUS`. This results in the native token not being transferred to the receiver and the user's bridge token being locked in the original layer.

The recommendation is to add an condition `nativeMappingValue` = `DEPLOYED_STATUS` for native token transfer in `confirmDeployment` by including the following code: 

```
if (nativeMappingValue == NATIVE_STATUS || nativeMappingValue == DEPLOYED_STATUS) {
   IERC20(_nativeToken).safeTransfer(_recipient, _amount);

```

The Linea team has implemented this recommendation in the pull request [66](https://github.com/Consensys/linea-token-bridge/pull/66) with the final commit hash as `8f8ee32cf3ad24ec669b62910d3d6eb1da9cc78e` and the bug has been resolved.

### Original Finding Content

#### Resolution



The recommendations are implemented by the Linea team in the pull request [66](https://github.com/Consensys/linea-token-bridge/pull/66) with the final commit hash as `8f8ee32cf3ad24ec669b62910d3d6eb1da9cc78e`


#### Description


If the bridge token B of a native token A is already deployed and `confirmDeployment` is called on the other layer and `setDeployed` sets A’s `nativeToBridgedToken` value to `DEPLOYED_STATUS`. The bridge token B cannot bridge to native token A in `completeBridging` function, because A’s `nativeToBridgedToken` value is not `NATIVE_STATUS`, as a result the native token won’t be transferred to the receiver. User’s bridge token will be locked in the original layer


#### Examples


**contracts/TokenBridge.sol:L217-L229**



```
if (nativeMappingValue == NATIVE\_STATUS) {
 // Token is native on the local chain
 IERC20(\_nativeToken).safeTransfer(\_recipient, \_amount);
} else {
 bridgedToken = nativeMappingValue;
 if (nativeMappingValue == EMPTY) {
 // New token
 bridgedToken = deployBridgedToken(\_nativeToken, \_tokenMetadata);
 bridgedToNativeToken[bridgedToken] = \_nativeToken;
 nativeToBridgedToken[\_nativeToken] = bridgedToken;
 }
 BridgedToken(bridgedToken).mint(\_recipient, \_amount);
}

```
**contracts/TokenBridge.sol:L272-L279**



```
function setDeployed(address[] memory \_nativeTokens) external onlyMessagingService fromRemoteTokenBridge {
 address nativeToken;
 for (uint256 i; i < \_nativeTokens.length; i++) {
 nativeToken = \_nativeTokens[i];
 nativeToBridgedToken[\_nativeTokens[i]] = DEPLOYED\_STATUS;
 emit TokenDeployed(\_nativeTokens[i]);
 }
}

```
#### Recommendation


Add an condition `nativeMappingValue` = `DEPLOYED_STATUS` for native token transfer in `confirmDeployment`



```
if (nativeMappingValue == NATIVE_STATUS || nativeMappingValue == DEPLOYED_STATUS) {
   IERC20(_nativeToken).safeTransfer(_recipient, _amount);

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Canonical Token Bridge |
| Report Date | N/A |
| Finders |  Tejaswa Rastogi
, Rai Yang |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/06/linea-canonical-token-bridge/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

