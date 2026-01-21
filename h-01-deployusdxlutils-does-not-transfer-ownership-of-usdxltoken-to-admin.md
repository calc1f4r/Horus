---
# Core Classification
protocol: HypurrFi_2025-02-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55465
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] `DeployUsdxlUtils` does not transfer ownership of usdxlToken to `admin`

### Overview


The reported bug is of medium severity and has a high likelihood of occurring. The function `_deployUsdxl` in the code deploys a token and sets the deployer as its owner. However, it fails to transfer the ownership to the admin after deployment and configuration. The recommended solution is to transfer the ownership of the token to the admin after deployment and configuration. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `_deployUsdxl` function, deploys usdxlTokenProxy and sets `deployer` as the owner of `usdxlToken`

```solidity
    function _deployUsdxl(address proxyAdmin, IDeployConfigTypes.HypurrDeployRegistry memory deployRegistry) internal {
        --snip--
        // 1. Deploy USDXL token implementation and proxy
        UpgradeableUsdxlToken usdxlTokenImpl = new UpgradeableUsdxlToken();

        bytes memory initParams = abi.encodeWithSignature("initialize(address)", deployer);

        usdxlTokenProxy = address(new TransparentUpgradeableProxy(address(usdxlTokenImpl), proxyAdmin, initParams));

        usdxlToken = IUsdxlToken(usdxlTokenProxy);

        --snip--
     }
```

But it does not transfer the ownership (admin rights) from `deployer` to `admin`

## Recommendations

Transfer ownership of `usdxlToken` to admin after deployment and config

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | HypurrFi_2025-02-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

