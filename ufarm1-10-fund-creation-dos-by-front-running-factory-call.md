---
# Core Classification
protocol: Ufarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62445
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[UFARM1-10] Fund creation DoS by front-running factory call

### Overview


The FundFactory contract has a function called `createFund` that is used to deploy a new contract called UFarmFund. This function is called from another contract called UFarmCore. However, there is a bug that allows anyone to use this function and deploy new UFarmFund contracts without proper authorization. This can lead to a denial of service attack and cause problems for the fund manager. To fix this bug, the `createFund` function should only be callable by the UFarmCore contract. This issue has been resolved.

### Original Finding Content

**Severity:** Medium

**Path:** FundFactory.sol:createFund#L47-L49

**Description:** The FundFactory exposes the `createFund` function, which uses a beacon proxy and `CREATE2` to deploy a new UFarmFund contract. This function is called from UFarmCore in the corresponding `createFund` function.

The `salt` value for the `CREATE2` opcode is the application ID, passed to the FundFactory from UFarmCore:
```
function createFund(
    address _fundManager,
    bytes32 _applicationId
)
    external override
    ownerOrHaveTwoPermissions(uint8(Permissions.UFarm.Member), uint8(Permissions.UFarm.ApproveFundCreation))
    nonReentrant returns (address fund)
{
    uint256 nextFundId = _funds.length();
    fund = fundFactory.createFund(_fundManager, _applicationId);
    _funds.add(fund);
    emit FundCreated(_applicationId, nextFundId, fund);
}
```
And in UFarmFactory it uses the SafeOPS library:
```
function createFund(address _manager, bytes32 _salt) external onlyLinked returns (address fund) {
    return SafeOPS._safeBeaconCreate2Deploy(fundImplBeacon, _salt, _getInitFundCall(_manager));
}

function _safeBeaconCreate2Deploy(
	address _beacon,
	bytes32 _salt,
	bytes memory _initCall
) internal returns (address addr) {
	try new BeaconProxy{salt: _salt}(_beacon, _initCall) returns (BeaconProxy beaconProxy) {
		return address(beaconProxy);
	} catch {
		revert BeaconProxyDeployFailed();
	}
}
```
The function reverts if the deployment fails, which would be the case if the contract already exists.

The `FundFactory.createFund` has no access control and as such, any attacker can deploy new UFarmFund contracts from the FundFactory. The newly deployed fund may not have been added to the UFarmCore fund whitelist, but the address and salt have now been taken.

By front-running application IDs in fund creation, an attacker can DoS fund creation, as the fund manager’s call would now revert.

**Remediation:**  We would recommend to gate the `FundFactory.createFund` function to be callable only by the UFarmCore contract. 

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Ufarm |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

