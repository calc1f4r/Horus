---
# Core Classification
protocol: Account Abstraction Schnorr MultiSig
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52620
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-multisig
source_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-multisig
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
  - Halborn
---

## Vulnerability Title

Missing sanity check for entryPoint

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `BasePaymaster` contract lacks interface validation for the \_entryPoint parameter in its constructor. The current implementation directly sets the `EntryPoint` address without verifying if it implements a matching `IEntryPoint` interface.

```
constructor(IEntryPoint _entryPoint, address _owner) Ownable(_owner) {

	//E @tocheck missing sanity check for _entryPoint

	setEntryPoint(_entryPoint);
}
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to implement the same mechanism as it is done in eth-infinitism [development branch](https://github.com/eth-infinitism/account-abstraction/blob/develop/contracts/core/EntryPoint.sol#L49) repository which includes proper validation with an interface to be implemented:

```
constructor(IEntryPoint _entryPoint) Ownable(msg.sender) {

	_validateEntryPointInterface(_entryPoint);
	
	entryPoint = _entryPoint;

}

function _validateEntryPointInterface(IEntryPoint _entryPoint) internal virtual {
   require(IERC165(address(_entryPoint)).supportsInterface(type(IEntryPoint).interfaceId), "IEntryPoint interface mismatch");
}
```

##### Remediation

**ACKNOWLEDGED:** An on chain version of this file will be used instead of the one in the repository, but the project does not use the affected code.

##### References

[RunOnFlux/account-abstraction/contracts/erc4337/core/BasePaymaster.sol#L19](https://github.com/RunOnFlux/account-abstraction/blob/master/contracts/erc4337/core/BasePaymaster.sol#L19)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Account Abstraction Schnorr MultiSig |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-multisig
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-multisig

### Keywords for Search

`vulnerability`

