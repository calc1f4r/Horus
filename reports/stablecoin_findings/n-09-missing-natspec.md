---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25180
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-connext
source_link: https://code4rena.com/reports/2022-06-connext
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-09] Missing NatSpec

### Overview

See description below for full details.

### Original Finding Content


```solidity
File: AssetFacet.sol
121:   /**
122:    * @notice Used to add supported assets. This is an admin only function
123:    * @dev When whitelisting the canonical asset, all representational assets would be
124:    * whitelisted as well. In the event you have a different adopted asset (i.e. PoS USDC
125:    * on polygon), you should *not* whitelist the adopted asset. The stable swap pool
126:    * address used should allow you to swap between the local <> adopted asset
127:    * @param _canonical - The canonical asset to add by id and domain. All representations
128:    * will be whitelisted as well
129:    * @param _adoptedAssetId - The used asset id for this domain (i.e. PoS USDC for
130:    * polygon)
131:    */
132:   function setupAsset(
133:     ConnextMessage.TokenId calldata _canonical,
134:     address _adoptedAssetId,
135:     address _stableSwapPool // @audit-info [INFO] NatSpec missing for _stableSwapPool
136:   ) external onlyOwner {
```

**[jakekidd (Connext) commented](https://github.com/code-423n4/2022-06-connext-findings/issues/263#issuecomment-1172807096):**
 > Great linking, great format!
>
> All of these seem non-critical except for L-14, which is acknowledged and L-02/L-11, which are valid.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-06-connext-findings/issues/263#issuecomment-1235169506):**
 > I would tend to agree that all of these are valid.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Connext |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-connext
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-06-connext

### Keywords for Search

`vulnerability`

