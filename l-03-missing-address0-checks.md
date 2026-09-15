---
# Core Classification
protocol: Mimo DeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4579
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-mimo-defi-contest
source_link: https://code4rena.com/reports/2022-04-mimo
github_link: #l-03-missing-address0-checks

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

[L-03] Missing address(0) checks

### Overview

See description below for full details.

### Original Finding Content


According to Slither:

```solidity
AdminInceptionVault.initialize(address,IAddressProvider,IDebtNotifier,IWETH,IERC20,IInceptionVaultsCore)._owner (contracts/inception/AdminInceptionVault.sol#36) lacks a zero-check on :
  - owner = _owner (contracts/inception/AdminInceptionVault.sol#48)
InceptionVaultsCore.initialize(address,IInceptionVaultsCore.VaultConfig,IERC20,IAddressProvider,IAdminInceptionVault,IInceptionVaultsDataProvider,IInceptionVaultPriceFeed)._owner (contracts/inception/InceptionVaultsCore.sol#41) lacks a zero-check on :
  - owner = _owner (contracts/inception/InceptionVaultsCore.sol#56)
DemandMinerV2.setFeeCollector(address).feeCollector (contracts/liquidityMining/v2/DemandMinerV2.sol#46) lacks a zero-check on :
  - _feeCollector = feeCollector (contracts/liquidityMining/v2/DemandMinerV2.sol#47)
PARMinerV2.liquidate(uint256,uint256,uint256,bytes).router (contracts/liquidityMining/v2/PARMinerV2.sol#124) lacks a zero-check on :
  - router.call(dexTxData) (contracts/liquidityMining/v2/PARMinerV2.sol#126)
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mimo DeFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-mimo
- **GitHub**: #l-03-missing-address0-checks
- **Contest**: https://code4rena.com/contests/2022-04-mimo-defi-contest

### Keywords for Search

`vulnerability`

