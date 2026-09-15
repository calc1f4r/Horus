---
# Core Classification
protocol: The Computable Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16575
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
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
finders_count: 3
finders:
  - Gustavo Grieco
  - Rajeev Gopalakrishna
  - Josselin Feist
---

## Vulnerability Title

Missing check for zero address in setPrivileged

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

## Target: Voting

### Difficulty: Medium

### Description
The `setPrivileged` function allows the data market owner to specify certain addresses as privileged contracts, which will then have exclusive access to certain functions. This is meant to be called once during initialization. In general, it is useful to add zero address checks for all such addresses, because uninitialized values in the EVM are zero values, and this check helps catch potential issues. Although the `setPrivileged` function checks for `0x0` address on the state variables (to ascertain that this is the first time they’re being initialized), it misses checking the parameters for `0x0` address, as shown in Figures 1 and 2.

```python
@public
def setPrivileged(reserve: address, listing: address):
    """
    @notice   We restrict some activities to only privileged contracts. Can only be called once.
    @dev      We only allow the owner to set the privileged address(es)
    @param    reserve   The deployed address of the reserve Contract
    @param    listing   The deployed address of the Listing Contract
    """
    assert msg.sender == self.owner_address
    assert self.listing_address == ZERO_ADDRESS
    assert self.reserve_address == ZERO_ADDRESS
    self.reserve_address = reserve
    self.listing_address = listing
```
**Figure 1:** setPrivileged function in MarketToken.vy

```python
@public
def setPrivileged(parameterizer: address, reserve: address, datatrust: address, listing: address):
    """
    @notice   Allow the Market owner to set privileged contract addresses. Can only be called once.
    """
    assert msg.sender == self.owner_address
    assert self.parameterizer_address == ZERO_ADDRESS
    assert self.reserve_address == ZERO_ADDRESS
    assert self.datatrust_address == ZERO_ADDRESS
    assert self.listing_address == ZERO_ADDRESS
    self.parameterizer_address = parameterizer
    self.reserve_address = reserve
    self.datatrust_address = datatrust
    self.listing_address = listing
```
**Figure 2:** setPrivileged function in Voting.vy

### Exploit Scenario
The data market owner accidentally uses `0x0` for one of the two parameters in `setPrivileged` of `MarketToken` for some of the four parameters in `setPrivileged` of `Voting`. The contract will then be in an incorrect and irrecoverable state because `setPrivilege` cannot be called again successfully; one of the asserts will always fail on the correctly set non-`0x0` address. The contract will have to be redeployed.

### Recommendation
Short term, add `0x0` address checks for all the address parameters in `setPrivilege`. This will prevent the contract from getting into an incorrect and irrecoverable state. Long term, use Echidna and Manticore to ensure that all the parameters are properly validated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | The Computable Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Rajeev Gopalakrishna, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf

### Keywords for Search

`vulnerability`

