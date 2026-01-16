---
# Core Classification
protocol: Reality Cards
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 289
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-06-reality-cards-contest
source_link: https://code4rena.com/reports/2021-06-realitycards
github_link: https://github.com/code-423n4/2021-06-realitycards-findings/issues/40

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - synthetics
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cmichel
  - shw
  - 0xRajeev
  - paulius.eth
---

## Vulnerability Title

[H-03] anyone can call function sponsor

### Overview


This bug report is about a vulnerability in a function called "sponsor" which should only be called by the factory but does not have any authentication checks. This means anyone can call it with an arbitrary sponsor address and transfer tokens from them if the allowance is greater than 0. The recommended mitigation step for this vulnerability is to check that the sender is a factory contract.

### Original Finding Content

## Handle

pauliax


## Vulnerability details

## Impact
This function sponsor should only be called by the factory, however, it does not have any auth checks, so that means anyone can call it with an arbitrary _sponsorAddress address and transfer tokens from them if the allowance is > 0:
    /// @notice ability to add liqudity to the pot without being able to win.
    /// @dev called by Factory during market creation
    /// @param _sponsorAddress the msgSender of createMarket in the Factory
    function sponsor(address _sponsorAddress, uint256 _amount)
        external
        override
    {
        _sponsor(_sponsorAddress, _amount);
    }

## Recommended Mitigation Steps
Check that the sender is a factory contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Reality Cards |
| Report Date | N/A |
| Finders | cmichel, shw, 0xRajeev, paulius.eth |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-realitycards
- **GitHub**: https://github.com/code-423n4/2021-06-realitycards-findings/issues/40
- **Contest**: https://code4rena.com/contests/2021-06-reality-cards-contest

### Keywords for Search

`Access Control`

