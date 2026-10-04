---
# Core Classification
protocol: Radius Technology EVMAuth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62871
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
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
  - Quan Nguyen Trail of Bits PUBLIC
---

## Vulnerability Title

TTL validation missing when updating burnable status

### Overview

See description below for full details.

### Original Finding Content

## Description

The `setBaseMetadata` function allows updating the burnable status of a token without validating whether a TTL (time-to-live) has been set. This creates a potential inconsistency where a token can be marked as non-burnable while still having an expiration time configured.

The contract enforces that TTL can be set only for burnable tokens in the `setTTL` function, but the reverse validation is missing. When updating a token’s metadata to make it non-burnable, the function should check if a TTL is currently set and either prevent the change or reset the TTL to zero. Without this validation, tokens can exist in an inconsistent state where they have expiration times but cannot be burned.

## Function

```solidity
function setBaseMetadata(uint256 id, bool _active, bool _burnable, bool _transferable) public {
    require(hasRole(TOKEN_MANAGER_ROLE, _msgSender()), "Unauthorized token manager");
    require(id <= nextTokenId, "Invalid token ID");
    _metadata[id] = BaseMetadata(id, _active, _burnable, _transferable);
    if (id == nextTokenId) {
        nextTokenId++;
    }
}
```

### Figure 7.1: Missing TTL validation in `setBaseMetadata` function

## Exploit Scenario

An admin sets up an authentication token with a 30-day TTL and burnable status. Later, the admin decides to make the token non-burnable by calling `setBaseMetadata` with `_burnable = false`. The token now has an inconsistent state where it has an expiration time but cannot be burned. This could lead to confusion in the system logic where non-burnable tokens can be burnt through the cleanup mechanisms.

## Recommendations

**Short term:** Add validation in the `setBaseMetadata` function to check if a TTL is set when making a token non-burnable, and either prevent the change or automatically reset the TTL to zero.

**Long term:** Implement comprehensive unit tests that cover metadata update scenarios, and ensure consistency between the burnable status and TTL configuration.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Radius Technology EVMAuth |
| Report Date | N/A |
| Finders | Quan Nguyen Trail of Bits PUBLIC |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf

### Keywords for Search

`vulnerability`

