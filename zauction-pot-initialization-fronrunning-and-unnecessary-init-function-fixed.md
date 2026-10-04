---
# Core Classification
protocol: Zer0 - zAuction
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13384
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/zer0-zauction/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - rwa
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Martin Ortner
---

## Vulnerability Title

zAuction - pot. initialization fronrunning and unnecessary init function ✓ Fixed

### Overview


This bug report concerns the zAuction contract, which has an unprotected initialization method that can be called by anyone. This could allow someone to monitor the mempool for new deployments of the contract and front-run the initialization to change its parameters. The deployer can detect this condition as subsequent calls to the initialization method will fail. The report recommends replacing the initialization method with a constructor, as the contract is not used in a proxy pattern. This would adhere to common interface naming conventions and the oz naming convention, where the method would be called "initialize".

### Original Finding Content

#### Resolution



Addressed with [zer0-os/[email protected]`135b2aa`](https://github.com/zer0-os/zAuction/commit/135b2aaddcfc70775fd1916518c2cc05106621ec) and the following statement:



> 
> 5.21 init deprecated, constructor added
> 
> 
> 




#### Description


The `zAuction` initialization method is unprotected and while only being executable once, can be called by anyone. This might allow someone to monitor the mempool for new deployments of this contract and fron-run the initialization to initialize it with different parameters.


A mitigating factor is that this condition can be detected by the deployer as subsequent calls to `init()` will fail.


* Note: this doesn’t adhere to common interface naming convention/oz naming convention where this method would be called `initialize`.
* Note: that zNS in contrast relies on ou/initializable pattern with proper naming.
* Note: that this function might not be necessary at all and should be replaced by a constructor instead, as the contract is not used with a proxy pattern.


#### Examples


**zAuction/contracts/zAuction.sol:L22-L26**



```
function init(address accountantaddress) external {
    require(!initialized);
    initialized = true;
    accountant = zAuctionAccountant(accountantaddress);
}

```
#### Recommendation


The contract is not used in a proxy pattern, hence, the initialization should be performed in the `constructor` instead.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Zer0 - zAuction |
| Report Date | N/A |
| Finders | David Oz Kashi, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/zer0-zauction/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

