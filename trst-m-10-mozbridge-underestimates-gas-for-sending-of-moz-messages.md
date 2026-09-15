---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: gas_limit

# Attack Vector Details
attack_type: gas_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19006
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - gas_limit

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-10 MozBridge underestimates gas for sending of Moz messages

### Overview


This bug report is about the bridge calculating LayerZero fees for sending Mozaic messages using an incorrect payload. The issue was that the actual payload used for Mozaic messages was longer than the one calculated by the bridge. This caused insufficient gas to be sent to the bridge, reverting the `send()` transaction. The recommended mitigation was to error on the side of caution and estimate a larger than expected fee. The team response was that the issue was fixed. The code now uses the correct payload for estimating fees.

### Original Finding Content

**Description:**
The bridge calculates LayerZero fees for sending Mozaic messages using the function below:
```solidity
        function quoteLayerZeroFee(uint16 _chainId, uint16 _msgType, LzTxObj memory _lzTxParams) public view returns (uint256 _nativeFee, uint256 _zroFee) { 
             bytes memory payload = "";
        if (_msgType == TYPE_REPORT_SNAPSHOT) {
                payload = abi.encode(TYPE_REPORT_SNAPSHOT);
        }
        else if (_msgType == TYPE_REQUEST_SNAPSHOT) {
                     payload = abi.encode(TYPE_REQUEST_SNAPSHOT);
        }
        else if (_msgType == TYPE_SWAP_REMOTE) {
                        payload = abi.encode(TYPE_SWAP_REMOTE);
        }
        else if (_msgType == TYPE_STAKE_ASSETS) {
                          payload = abi.encode(TYPE_STAKE_ASSETS);
        }   
        else if (_msgType == TYPE_UNSTAKE_ASSETS) {
                                 payload = abi.encode(TYPE_UNSTAKE_ASSETS);
        }
        else if (_msgType == TYPE_REPORT_SETTLE) {
                                 payload = abi.encode(TYPE_REPORT_SETTLE);
        }
        else if (_msgType == TYPE_REQUEST_SETTLE) {
                            payload = abi.encode(TYPE_REQUEST_SETTLE);
        }
        else {
                         revert("MozBridge: unsupported function type");
        }
        
                     bytes memory _adapterParams = _txParamBuilder(_chainId, _msgType, _lzTxParams);
              return layerZeroEndpoint.estimateFees(_chainId, address(this), 
       payload, useLayerZeroToken, _adapterParams);
        }
```
The issue is that the actual payload used for Mozaic messages is longer than the one calculated 
above. For example, REPORT_SNAPSHOT messages include a **Snapshot** structure.
 ```solidity
            struct Snapshot {
               uint256 depositRequestAmount;
                 uint256 withdrawRequestAmountMLP;
                     uint256 totalStablecoin;
                         uint256 totalMozaicLp; // Mozaic "LP"
                             uint8[] pluginIds;
                                 address[] rewardTokens;
                                  uint256[] amounts;
                   }
```
Undercalculation of gas fees will cause insufficient gas to be sent to the bridge, reverting the 
`send()` transaction. 

**Recommended mitigation:**
Error on the side of caution and estimate a larger than expected fee.

**Team response:**
Fixed.

**Mitigation review:**
The code now uses the correct payload for estimating fees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Gas Limit`

