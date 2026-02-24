---
# Core Classification
protocol: MonoX
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50182
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 0

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

ROLE-BASED ACCESS CONTROL MISSING

### Overview


The report highlights a bug in a smart contract called Monoswap.sol. This contract is used for accessing and managing tokens. The bug relates to the Access Control policy, which is important for maintaining security and decentralization in the contract. The code for the contract is given, and the bug is identified in the function "updatePoolPrice". The bug allows anyone to update the pool price, instead of just the owner. This can lead to unauthorized changes in the contract and compromise its security. The bug has been given a score of 4 for impact and likelihood, indicating that it is a significant issue that needs to be addressed. The recommendation for fixing the bug is to introduce new roles in the contract, which has been done in a recent update.

### Original Finding Content

##### Description

In smart contracts, implementing a correct Access Control policy is an essential step to maintain security and decentralization for permissions on a token. All the features of the smart contract , such as mint/burn tokens and pause contracts are given by Access Control. For instance, Ownership is the most common form of Access Control. In other words, the owner of a contract (the account that deployed it by default) can do some administrative tasks on it. Nevertheless, other authorization levels are required to follow the principle of least privilege, also known as least authority. Briefly, any process, user or program only can access to the necessary resources or information. Otherwise, the ownership role is useful in a simple system, but more complex projects require the use of more roles by using Role-based access control.

Code Location
-------------

#### Monoswap.sol

```
function setFeeTo (address _feeTo) onlyOwner external {
    feeTo = _feeTo;
}

function setFees (uint16 _fees) onlyOwner external {
    require(_fees<1e3, "fees too large");
    fees = _fees;
}

function setDevFee (uint16 _devFee) onlyOwner external {
    require(_devFee<1e3, "devFee too large");
    devFee = _devFee;
}

// update status of a pool. onlyOwner.
function updatePoolStatus(address _token, PoolStatus _status) public onlyOwner {
    PoolInfo storage pool = pools[_token];
    pool.status = _status;
}

/**
 @dev update pools price if there were no active trading for the last 6000 blocks
 @notice Only owner callable, new price can neither be 0 nor be equal to old one
 @param _token pool identifider (token address)
 @param _newPrice new price in wei (uint112)
*/
function updatePoolPrice(address _token, uint112 _newPrice) public onlyOwner {
    require(_newPrice > 0, 'Monoswap: zeroPriceNotAccept');

```

##### Score

Impact: 4  
Likelihood: 4

##### Recommendation

**SOLVED**: Fixed in commit #635a4cee2f2e50d854e06cac47c48aa0fafde2b0. Several new roles were introduced.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | MonoX |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment

### Keywords for Search

`Access Control`

