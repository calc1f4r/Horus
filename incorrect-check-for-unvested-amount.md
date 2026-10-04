---
# Core Classification
protocol: VTVL
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47913
audit_firm: OtterSec
contest_link: https://vtvl.io/
source_link: https://vtvl.io/
github_link: https://github.com/VTVL-co/vtvl-smart-contracts/tree/audit-ready-jul-23

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
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Incorrect Check For Unvested Amount

### Overview

The bug report discusses an issue in the VTVLVesting smart contract where the revokeClaim function may fail to prevent the revocation of a claim that has been fully consumed. This occurs when a user has not claimed the amount after the vesting period has ended. The report suggests a modification to the verification process to correctly handle this situation and provides a patch for the issue. The issue has been fixed in recent commits to the contract.

### Original Finding Content

## VTVLVesting::revokeClaim Vulnerability Overview

In `VTVLVesting::revokeClaim`, `amountWithdrawn` for the claim is compared to `finalVestAmt` to prevent the revocation of a claim that has been fully consumed. This method will fail when a user has not claimed the amount after the vesting was completed, as even in this case, `_claim.amountWithdrawn < finalVestAmt` will result in true.

## VTVLVesting.sol Solidity Code Snippet

```solidity
function revokeClaim(
    address _recipient,
    uint256 _scheduleIndex
) external onlyOwner hasActiveClaim(_recipient, _scheduleIndex) {
    // Fetch the claim
    Claim storage _claim = claims[_recipient][_scheduleIndex];
    // Calculate what the claim should finally vest to
    uint256 finalVestAmt = finalVestedAmount(_recipient, _scheduleIndex);
    // No point in revoking something that has been fully consumed
    // so require that there be unconsumed amount
    require(_claim.amountWithdrawn < finalVestAmt, "NO_UNVESTED_AMOUNT");
    [...]
}
```

## Remediation

Replace the current verification of the consumed amount utilizing `_claim.amountWithdrawn` with `vestedSoFarAmt` in the required statement. This modification will correctly handle situations where the user does not withdraw the amount, but the vesting period has elapsed, as `vestedSoFarAmt` will always be greater than or equal to `finalVestAmt`.

## Updated VTVLVesting.sol Solidity Code Snippet

```solidity
function revokeClaim(
    address _recipient,
    uint256 _scheduleIndex
) external onlyOwner hasActiveClaim(_recipient, _scheduleIndex) {
    // Fetch the claim
    Claim storage _claim = claims[_recipient][_scheduleIndex];
    // Calculate what the claim should finally vest to
    uint256 finalVestAmt = finalVestedAmount(_recipient, _scheduleIndex);
    uint256 vestedSoFarAmt = vestedAmount(
        _recipient,
        _scheduleIndex,
        uint40(block.timestamp)
    );
    // No point in revoking something that has been fully consumed
    // so require that there be unconsumed amount
    require(vestedSoFarAmt < finalVestAmt, "NO_UNVESTED_AMOUNT");
    [...]
}
```

## Patch

Fixed in commits `cfb17bc` and `56f3e40` by allowing the withdraw function to be utilized on revoked claims, enabling the claimants to retrieve the remaining vested amount that was not withdrawn before the claim was revoked.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | VTVL |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://vtvl.io/
- **GitHub**: https://github.com/VTVL-co/vtvl-smart-contracts/tree/audit-ready-jul-23
- **Contest**: https://vtvl.io/

### Keywords for Search

`vulnerability`

