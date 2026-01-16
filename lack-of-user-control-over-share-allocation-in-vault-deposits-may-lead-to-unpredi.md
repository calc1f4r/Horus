---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54335
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
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
finders_count: 4
finders:
  - solthodox
  - elhaj
  - hals
  - Shaheen
---

## Vulnerability Title

Lack of user control over share allocation in vault deposits may lead to unpredictable out- comes 

### Overview


This bug report highlights a vulnerability in a protocol where the number of shares minted for a user upon deposit may not align with their expectations. This can be problematic for vaults that use external protocols, as changes in the external protocol's conditions could result in front-running attacks. The report recommends giving users the ability to specify their desired amount of shares when depositing to a superForm to mitigate this risk.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The protocol lacks validation to ensure that the number of shares minted by a vault upon deposit aligns with the user's expectations, and the users have no choice but to accept any amount of shares resulted when depositing to a vault. This is particularly concerning for vaults that implement additional deposit strategies, which could be susceptible to front-running or other market manipulations.

For example, a vault might use the deposited assets to engage in yield farming activities, where the number of shares minted to the depositor is dependent on the current state of the external protocol. If this protocol's conditions change rapidly (such as through front-running), the current protocol design exposes the users to front running attacks.

See the following example from the `_processDirectDeposit` function of a superForm:

```solidity
function _processDirectDeposit(InitSingleVaultData memory singleVaultData_) internal returns (uint256 dstAmount) {
    // prev code ....
    if (singleVaultData_.retain4626) {
        //@audit : user can ' t refuse the amount of shares minted even if it ' s zero .
        // see the line below
        dstAmount = v.deposit(vars.assetDifference, singleVaultData_.receiverAddress);
    } else {
        // see the line below
        dstAmount = v.deposit(vars.assetDifference, address(this));
    }
}
```

```solidity
function _directSingleDeposit(address srcSender_, bytes memory permit2data_, InitSingleVaultData memory vaultData_) internal virtual {
    // prev code ...
    // @audit : the contract mint any amount resulted from depositing , and the user have no control of that
    // see the line below
    if (dstAmount != 0 && !vaultData_.retain4626) {
        /// @dev mint super positions at the end of the deposit action if user doesn ' t retain 4626
        ISuperPositions(superRegistry.getAddress(keccak256("SUPER_POSITIONS"))).mintSingle(
            srcSender_, vaultData_.superformId, dstAmount
        );
    }
}
```

This could lead to users receiving fewer shares than anticipated if the vault's share price is affected by other on-chain activities.

## Recommendation
To mitigate this risk, the user should have the ability to specify their desired minted amount of shares when they are depositing to a superForm.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | solthodox, elhaj, hals, Shaheen |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

