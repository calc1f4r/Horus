---
# Core Classification
protocol: Opendollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34076
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/OpenDollar-security-review.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] An Authorized user can remove himself from authorization

### Overview

See description below for full details.

### Original Finding Content

In Authorizable.sol, there is a function `removeAuthorization()` whereby an Authorized user can remove authorization from an authorized account.

```
  function removeAuthorization(address _account) external virtual isAuthorized {
    _removeAuthorization(_account);
  }
```

There is no check to make sure the authorized user cannot remove himself. If the authorized user removes himself accidentally and there are no more users with authorization, there is no way to get back authorization since someone needs to be authorized to call `addAuthorization()`

This will affect the deployment of the Relayers as it is under the `isAuthorized` modifier.

```
  function deployChainlinkRelayer(
    address _aggregator,
    uint256 _staleThreshold
> ) external isAuthorized returns (IBaseOracle _chainlinkRelayer) {
    _chainlinkRelayer = IBaseOracle(address(new ChainlinkRelayerChild(_aggregator, _staleThreshold)));
    relayerId++;
```

Make sure the authorized user cannot withdraw his authorization and make sure there is always someone with authorization.

**Open Dollar comments**

_We recognize that an authorized account can be removed, and further modifications could be prevented. There is no risk to the protocol since a new factory could be deployed at any time if authorization is lost._

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Opendollar |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/OpenDollar-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

