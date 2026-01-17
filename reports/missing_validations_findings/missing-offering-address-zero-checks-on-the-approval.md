---
# Core Classification
protocol: Plural Energy Offering
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51211
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/plural-energy/plural-energy-offering
source_link: https://www.halborn.com/audits/plural-energy/plural-energy-offering
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

Missing offering address zero checks on the approval

### Overview

See description below for full details.

### Original Finding Content

##### Description

During the assessment it has been observed than the `offeringAddress` is not properly validated. If the offering is deleted and after approved, the EVM revert is triggered due to the `safeApprove` function is using as second parameter the address zero due to empty index mapping after deletion getter (`getOffering` function).

```
/// @inheritdoc IAssetTokenVendor
    function approveOffering(
        address assetToken,
        uint32 offeringNum
    ) public override onlyOwner {
        address offeringAddress = getOffering(assetToken, offeringNum);

        // Ensure compliance rules are updated for the new offering
        IAssetToken _assetToken = IAssetToken(assetToken);
        ICompliance compliance = ICompliance(_assetToken.compliance());
        address[] memory tokenAddresses = new address[](1);
        tokenAddresses[0] = assetToken;
        string memory allowedRole = Roles.OFFERING;
        string[] memory roles = new string[](1);
        roles[0] = allowedRole;

        compliance.addAllowedRolesToTokens(tokenAddresses, roles);
        compliance.addRoleToAccount(allowedRole, offeringAddress);

        // Approve offering to transfer up to the number of tokens for sale
        IERC20(assetToken).safeApprove(
            offeringAddress,
            IOffering(offeringAddress).numTokensForSale()
        );
    }
```

##### BVSS

[AO:A/AC:H/AX:H/C:M/I:N/A:N/D:N/Y:N/R:N/S:U (0.5)](/bvss?q=AO:A/AC:H/AX:H/C:M/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

Ensure zero address check in the case the offering is 0 due to deletion or not existing offering.

### Remediation Plan

**SOLVED :** The **Plural Energy team** solved the issue by adding proper checks.

```
if (offeringAddress == address(0)) {
            revert OfferingNotFound(assetToken, offeringNum);
}
```

##### Remediation Hash

<https://github.com/plural-energy/plural-protocol/commit/7094bddfab5804faa5d31ad63891238ca1dfabd5>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Plural Energy Offering |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/plural-energy/plural-energy-offering
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/plural-energy/plural-energy-offering

### Keywords for Search

`vulnerability`

