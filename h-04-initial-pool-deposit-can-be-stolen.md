---
# Core Classification
protocol: InsureDAO
chain: everychain
category: economic
vulnerability_type: initialization

# Attack Vector Details
attack_type: initialization
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1297
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/250

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - initialization
  - front-running

protocol_categories:
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - cmichel
---

## Vulnerability Title

[H-04] Initial pool deposit can be stolen

### Overview


This bug report is about a vulnerability in the PoolTemplate.initialize function, which is called when creating a market with Factory.createMarket. This function calls a vault function to transfer an initial deposit amount from the initial depositor, but the initial depositor needs to first approve the vault contract for the transferFrom to succeed. An attacker can then frontrun the Factory.createMarket transaction with their own market creation and create a market with different parameters, but still passing in the same initial deposit amount and initial depositor. This means the initial depositor's tokens are essentially lost, as they can be used to create a market with parameters they did not want.

To mitigate this vulnerability, it is recommended that the initial depositor be set to Factory.createMarket's msg.sender, instead of being able to pick a whitelisted one as _references[4]. This would prevent the attacker from frontrunning the Factory.createMarket transaction and creating a market with different parameters.

### Original Finding Content

_Submitted by cmichel, also found by WatchPug_

Note that the `PoolTemplate.initialize` function, called when creating a market with `Factory.createMarket`, calls a vault function to transfer an initial deposit amount (`conditions[1]`) *from* the initial depositor (`_references[4]`):

```solidity
// PoolTemplate
function initialize(
     string calldata _metaData,
     uint256[] calldata _conditions,
     address[] calldata _references
) external override {
     // ...

     if (_conditions[1] > 0) {
          // @audit vault calls asset.transferFrom(_references[4], vault, _conditions[1])
          _depositFrom(_conditions[1], _references[4]);
     }
}

function _depositFrom(uint256 _amount, address _from)
     internal
     returns (uint256 _mintAmount)
{
     require(
          marketStatus == MarketStatus.Trading && paused == false,
          "ERROR: DEPOSIT_DISABLED"
     );
     require(_amount > 0, "ERROR: DEPOSIT_ZERO");

     _mintAmount = worth(_amount);
     // @audit vault calls asset.transferFrom(_from, vault, _amount)
     vault.addValue(_amount, _from, address(this));

     emit Deposit(_from, _amount, _mintAmount);

     //mint iToken
     _mint(_from, _mintAmount);
}
```

The initial depositor needs to first approve the vault contract for the `transferFrom` to succeed.

An attacker can then frontrun the `Factory.createMarket` transaction with their own market creation (it does not have access restrictions) and create a market *with different parameters* but still passing in `_conditions[1]=amount` and `_references[4]=victim`.

A market with parameters that the initial depositor did not want (different underlying, old whitelisted registry/parameter contract, etc.) can be created with their tokens and these tokens are essentially lost.

#### Recommended Mitigation Steps

Can the initial depositor be set to `Factory.createMarket`'s `msg.sender`, instead of being able to pick a whitelisted one as `_references[4]`?

**[oishun1112 (Insure) confirmed](https://github.com/code-423n4/2022-01-insure-findings/issues/250):**
 > https://github.com/code-423n4/2022-01-insure-findings/issues/224




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | WatchPug, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/250
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`Initialization, Front-Running`

