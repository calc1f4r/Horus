---
# Core Classification
protocol: Spokes V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51916
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/spokes-v1
source_link: https://www.halborn.com/audits/concrete/spokes-v1
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
  - Halborn
---

## Vulnerability Title

Remote Protocol Proxies Unable To Execute Core Functions

### Overview


The bug report discusses a problem with the `openProtection`, `SupplyAndProtect`, and `SupplyBorrowAndProtect` functions in the UserBase contract. These functions have similar logic to check if the caller is authorized to perform the intended operation. However, the logic incorrectly restricts the execution of the function's core logic to only when the caller is the protocol endpoint. This means that valid remote proxies are unable to execute their intended functionality, causing disruptions or unintended denials of service. The report recommends modifying the access control logic to allow both the protocol endpoint and remote proxies to execute the functions and implementing a function for remote proxies to claim rewards. The bug has been solved by the Concrete team and the code has been updated. 

### Original Finding Content

##### Description

The `openProtection`, `SupplyAndProtect`, and `SupplyBorrowAndProtect` functions from the UserBase contract utilize similar logic to validate whether the caller is authorized to perform the intended operation. The logic begins by checking if the caller is the protocol endpoint using `_callerIsEndpoint` method. If this check is true, it sets the `callerIsProtocol` flag. Additionally, the logic checks if the caller is a remote protocol proxy using `callerIsRemoteProtocolProxy` and combines these two checks to determine if the existing protection can be overwritten.

```
        bool callerIsProtocol = _callerIsEndpoint();
        bool mayOverwriteExistingProtection = _callerIsRemoteProtocolProxy() || callerIsProtocol;
        if (_getProtectionInfo() != 0 && !mayOverwriteExistingProtection) {
            revert Errors.ProtectionAlreadyOpened();
        }
        if (callerIsProtocol) {
	        LOGIC HERE
            );
        } else {
            revert Errors.NotProtocolAndNotIntervenable();
        }
```

However, the logic incorrectly restricts the execution of the function's core logic to only when the caller is the protocol endpoint. If the caller is a valid remote proxy, the function will incorrectly prevent the remote proxy from executing its intended functionality, causing disruptions or unintended denials of service.

##### Proof of Concept

```
    function test_remoteProtocolProxyReverts() external {
        address userBlueprint = _createAaveV3UserBlueprint();
        vm.prank(address(cccm));
            IUserIntervention(userBlueprint).setBorrowToken(address(usdc));
        uint256 supplyAmount = 1000 ether;
        uint256 borrowAmount = 1_500_000 * 10 ** 6;
        (uint256 encodedProtectionInfo, uint256 promisedAmountInCollateral) =
            _createConcreteProtectionEncoding(supplyAmount, borrowAmount);

        //Expect a revert if the remote proxy is the caller
        vm.prank(address(remoteProtocolProxy));
            vm.expectRevert(Errors.NotProtocolAndNotIntervenable.selector);
            IProtocolIntervention(userBlueprint).openProtection(
                encodedProtectionInfo, concreteForeclosureFeeDebtFractionInWad, promisedAmountInCollateral);

        vm.prank(address(remoteProtocolProxy));
            vm.expectRevert(Errors.NotProtocolAndNotIntervenable.selector);
            IProtocolIntervention(userBlueprint).supplyAndProtect(
                supplyAmount, encodedProtectionInfo, liteForeclosureFeeFractionInWad, promisedAmountInCollateral);

        vm.prank(address(remoteProtocolProxy));
            vm.expectRevert(Errors.NotProtocolAndNotIntervenable.selector);
            IProtocolIntervention(userBlueprint).supplyBorrowAndProtect(
                supplyAmount, borrowAmount, address(usdc), encodedProtectionInfo, liteForeclosureFeeFractionInWad, promisedAmountInCollateral);
    }
```

  
![](https://halbornmainframe.com/proxy/audits/images/66ced811c5aca51c428ede22)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:N/Y:N/R:N/S:U)

##### Recommendation

Modify the access control logic to ensure that both the protocol endpoint and the remote proxy are allowed to execute the functions. Implement a function that allows the Remote Proxy to claim rewards as intended by the logic of the `claimRewards` function.

##### Remediation

**SOLVED:** The **Concrete team** solved the issue. The mentioned logic was removed from the functions.

##### Remediation Hash

<https://github.com/Blueprint-Finance/sc_spokes-v1/commit/cb3429119651a43f0e189a11cb9c7cdf88495e23>

##### References

[Blueprint-Finance/sc\_spokes-v1/src/userBase/UserBase.sol#L389-L408](https://github.com/Blueprint-Finance/sc_spokes-v1/blob/984a7f00cf76281bd56278d4991b7676e151a792/src/userBase/UserBase.sol#L389-L408)

[Blueprint-Finance/sc\_spokes-v1/src/userBase/UserBase.sol#L419-L437](https://github.com/Blueprint-Finance/sc_spokes-v1/blob/984a7f00cf76281bd56278d4991b7676e151a792/src/userBase/UserBase.sol#L419-L437)

[Blueprint-Finance/sc\_spokes-v1/src/userBase/UserBase.sol#L459-L480](https://github.com/Blueprint-Finance/sc_spokes-v1/blob/984a7f00cf76281bd56278d4991b7676e151a792/src/userBase/UserBase.sol#L459-L480)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Spokes V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/spokes-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/spokes-v1

### Keywords for Search

`vulnerability`

