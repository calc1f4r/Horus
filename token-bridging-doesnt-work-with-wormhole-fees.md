---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28186
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#1-token-bridging-doesnt-work-with-wormhole-fees
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
  - MixBytes
---

## Vulnerability Title

Token Bridging doesn't work with Wormhole fees

### Overview


The bug report describes an issue with the `transferTokens()` function of type `payable` on line 93 of the Bridge.sol file. The problem is that the `publishMessage()` function of type `payable` on line 151 requires a condition for payment of the commission to be met, but in the checked contract, at line 49 of the BridgeConnectorWormhole.vy file, there is no `@payable` modifier anywhere and no `msg.value` value handling. As a result, the `submit ()` and `collect_rewards ()` functions will not work in the `AnchorVault.vy` contract, because there is no commission fee for the `Wormhole` system.

The recommendation is to add a commission payment for the `Wormhole` system in order to ensure that the `submit ()` and `collect_rewards ()` functions work as expected.

### Original Finding Content

##### Description
Line 
- https://github.com/certusone/wormhole/blob/9bc408ca1912e7000c5c2085215be9d44713028b/ethereum/contracts/bridge/Bridge.sol#L93
has a `transferTokens ()` function of type `payable`. In the body of this function, on line 133, a call to the internal 
function `logTransfer ()` is made and one of the parameters `msg.value` is passed.
At line  
- https://github.com/certusone/wormhole/blob/9bc408ca1912e7000c5c2085215be9d44713028b/ethereum/contracts/bridge/Bridge.sol#L151
from the `logTransfer()` function, the `publishMessage()` function is called.
The `publishMessage()` function of type `payable` on the line:
- https://github.com/certusone/wormhole/blob/9bc408ca1912e7000c5c2085215be9d44713028b/ethereum/contracts/Implementation.sol#L21
the condition for payment of the commission must be met.
```
   require(msg.value == messageFee(), "invalid fee");
```

In the checked contract, at line 
- https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/BridgeConnectorWormhole.vy#L49
a call to the `transferTokens()` function from the `_transfer_asset()` function is made. 
But there is no `@payable` modifier anywhere and no `msg.value` value handling.
Therefore, the `_transfer_asset()` function will not work.
As a result, the `submit ()` and `collect_rewards ()` functions will not work in the `AnchorVault.vy` contract, 
because there is no commission fee for the `Wormhole` system.
##### Recommendation
It is required to add a commission payment for the `Wormhole` system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#1-token-bridging-doesnt-work-with-wormhole-fees
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

