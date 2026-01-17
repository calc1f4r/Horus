---
# Core Classification
protocol: Subsquid
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58248
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:
  - access_control

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Lack of access control on tSQD's `registerTokenOnL2`

### Overview


This bug report highlights a potential issue in the tSQD system, where an attacker could change the address of the L2 token and cause problems with the bridge token. This could have a high impact and is likely to occur. The `registerTokenOnL2` function is currently not restricted, allowing an attacker to front-run and input an incorrect address for the L2 token. This would result in the bridge token being broken and unable to be changed within the gateway. The recommendation is to use the Ownable functionality and restrict the `registerTokenOnL2` function to only be called by the owner/admin, as suggested by the design of the Arbitrum bridge token.

### Original Finding Content

## Severity

**Impact**: High, malicious attacker can set L2 custom address to different address to break the bridge token.

**Likelihood**: Medium, attacker can front-ran the `registerTokenOnL2` to break the bridge token.

## Description

tSQD is designed so that it can be bridged from Ethereum (L1) to Arbitrum (L2) via Arbitrum’s generic-custom gateway.
However, the `registerTokenOnL2` function, which sets the L2 token address via `gateway.registerTokenToL2`, is not currently restricted.

```solidity
  function registerTokenOnL2(
    address l2CustomTokenAddress,
    uint256 maxSubmissionCostForCustomGateway,
    uint256 maxSubmissionCostForRouter,
    uint256 maxGasForCustomGateway,
    uint256 maxGasForRouter,
    uint256 gasPriceBid,
    uint256 valueForGateway,
    uint256 valueForRouter,
    address creditBackAddress
  ) public payable {
    require(!shouldRegisterGateway, "ALREADY_REGISTERED");
    shouldRegisterGateway = true;

    gateway.registerTokenToL2{value: valueForGateway}(
      l2CustomTokenAddress, maxGasForCustomGateway, gasPriceBid, maxSubmissionCostForCustomGateway, creditBackAddress
    );

    router.setGateway{value: valueForRouter}(
      address(gateway), maxGasForRouter, gasPriceBid, maxSubmissionCostForRouter, creditBackAddress
    );

    shouldRegisterGateway = false;
  }
```

An attacker can front-run the `registerTokenOnL2` and put an incorrect address for `l2CustomTokenAddress` to break the bridge token. Once it is called, the L2 token cannot be changed inside the gateway.

## Recommendations

Use the Ownable functionality inside tSQD and restrict `registerTokenOnL2` so that it can only be called by the owner/admin, as suggested by the Arbitrum bridge token design.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Subsquid |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Access Control`

