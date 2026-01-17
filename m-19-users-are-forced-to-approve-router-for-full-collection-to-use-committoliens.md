---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25835
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/283

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

[M-19] Users are forced to approve Router for full collection to use commitToLiens() function

### Overview


This bug report was filed for the code-423n4/2023-01-astaria repository. The bug was found in the Router#commitToLiens() function. It was observed that the Router must be approved for all, which is a level of approvals that many users are not comfortable with.

The bug was found in the following lines of code:

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/AstariaRouter.sol#L780-L785><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L287-L306><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L233-L244>

The check in the code allows the following situations pass:

*   caller of the function == owner of the NFT
*   receiver of the loan == owner of the NFT
*   receiver of the loan == address approved for the individual NFT
*   caller of the function == address approved for all

This is inconsistent and doesn't make much sense. The approved users should have the same permissions. The most common flow (that the address approved for the individual NFT — the Router — is the caller) does not work and will lead to the function reverting.

The recommended mitigation step is to change the check to include `msg.sender != operator` rather than `receiver != operator`. SantiagoGregory (Astaria) confirmed the bug and Picodes (judge) commented that the severity should remain medium, considering this is a broken functionality.

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/AstariaRouter.sol#L780-L785><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L287-L306><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L233-L244>

When a user calls Router#commitToLiens(), the Router calls `commitToLien()`. The comments specify:

`//router must be approved for the collateral to take a loan,`

However, the Router being approved isn't enough. It must be approved for all, which is a level of approvals that many users are not comfortable with. This is because, when the commitment is validated, it is checked as follows:

        uint256 collateralId = params.tokenContract.computeId(params.tokenId);
        ERC721 CT = ERC721(address(COLLATERAL_TOKEN()));
        address holder = CT.ownerOf(collateralId);
        address operator = CT.getApproved(collateralId);
        if (
          msg.sender != holder &&
          receiver != holder &&
          receiver != operator &&
          !CT.isApprovedForAll(holder, msg.sender)
        ) {
          revert InvalidRequest(InvalidRequestReason.NO_AUTHORITY);
        }

### Proof of Concept

The check above allows the following situations pass:

*   caller of the function == owner of the NFT
*   receiver of the loan == owner of the NFT
*   receiver of the loan == address approved for the individual NFT
*   caller of the function == address approved for all

This is inconsistent and doesn't make much sense. The approved users should have the same permissions.

More importantly, the most common flow (that the address approved for the individual NFT — the Router — is the caller) does not work and will lead to the function reverting.

### Recommended Mitigation Steps

Change the check to include `msg.sender != operator` rather than `receiver != operator`.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/283)**

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/283#issuecomment-1439014063):**
 > Keeping medium severity, considering this is a broken functionality.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/283
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

