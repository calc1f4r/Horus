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
solodit_id: 26795
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

User Cannot Withdraw Funds if Bridging Failed or Delayed  Won't Fix

### Overview


A bug has been reported in the TokenBridge contract, which is part of the bridge token contract. If bridging fails due to a single coordinator being down, censoring messages or the bridge token contract being set to a bad or wrong contract address, users' funds will be stuck in the TokenBridge contract until the coordinator is online or stops censoring. There is currently no way to withdraw the deposited funds.

The code snippet for the setCustomContract function is provided as an example. It allows the owner to set a custom native token and target contract address.

The recommendation is to add withdraw functionality to let users withdraw their funds in the above circumstances, or at least add withdraw functionality for an admin, who can manually send the funds to the user. Ultimately, the coordinator and sequencer should be decentralized to reduce the risk of bridging failure.

### Original Finding Content

#### Description


If the bridging failed due to the single coordinator is down, censoring the message, or bridge token contract is set to a bad or wrong contract address by `setCustomContract`, user’s funds will stuck in the `TokenBridge` contract until coordinator is online or stop censoring, there is no way to withdraw the deposited funds


#### Examples


**contracts/TokenBridge.sol:L341-L348**



```
function setCustomContract(
 address \_nativeToken,
 address \_targetContract
) external onlyOwner isNewToken(\_nativeToken) {
 nativeToBridgedToken[\_nativeToken] = \_targetContract;
 bridgedToNativeToken[\_targetContract] = \_nativeToken;
 emit CustomContractSet(\_nativeToken, \_targetContract);
}

```
#### Recommendation


Add withdraw functionality to let user withdraw the funds under above circumstances or at least add withdraw functionality for Admin (admin can send the funds to the user manually), ultimately decentralize coordinator and sequencer to reduce bridging failure risk.

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

