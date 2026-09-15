---
# Core Classification
protocol: Eclipse Canonical Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47140
audit_firm: OtterSec
contest_link: https://www.eclipse.xyz/
source_link: https://www.eclipse.xyz/
github_link: https://github.com/Eclipse-Laboratories-Inc

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
finders_count: 2
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
---

## Vulnerability Title

Underestimated Minimum Rent Deposit

### Overview


The EtherBridge contract has a vulnerability where the calculation of MIN_DEPOSIT_LAMPORTS does not account for the necessary ACCOUNT_STORAGE_OVERHEAD of 128. This means that deposits made may not be considered rent-exempt according to Solana's standards. The issue has been resolved in a recent patch by hard-coding MIN_DEPOSIT_LAMPORTS to a sufficient amount. To fix this issue, MIN_DEPOSIT_LAMPORTS should be recalculated to include ACCOUNT_STORAGE_OVERHEAD and validated against Solana's CLI tools or official documentation.

### Original Finding Content

## Vulnerability in EtherBridge

The vulnerability in EtherBridge arises from an incorrect calculation of `MIN_DEPOSIT_LAMPORTS`, which is necessary for determining the minimum deposit requirement in terms of Solana’s rent system. The calculation of `MIN_DEPOSIT_LAMPORTS` does not account for the `ACCOUNT_STORAGE_OVERHEAD` of 128, which is essential in Solana’s rent calculation to determine the minimum balance required for rent exemption. Without including `ACCOUNT_STORAGE_OVERHEAD`, `MIN_DEPOSIT_LAMPORTS` may result in an amount that is lower than what is actually required by Solana’s rent system. This may result in deposits that are not rent-exempt according to Solana’s standards.

> _EtherBridge.sol solidity_
>
> ```solidity
> /// @title EtherBridge
> /// @dev A bridge contract for depositing and withdrawing ether to and from the Eclipse rollup.
> contract EtherBridge is
> [...]
> {
> bytes32 public constant ETHER_BRIDGE_ID = keccak256("EtherBridge");
> /// @dev Calculation of constants for minimum deposit requirements.
> /// `MIN_DEPOSIT_LAMPORTS` ensures deposit data on Solar Eclipse is rent-exempt, based on:
> /// These constants ensure deposit amounts meet Solar Eclipse's rent-exemption criteria,
> ,→ adapted for Ethereum's context.
> uint256 public constant MIN_DEPOSIT = MIN_DEPOSIT_LAMPORTS * WEI_PER_LAMPORT;
> [...]
> }
> ```

## Remediation

Ensure that `MIN_DEPOSIT_LAMPORTS` is recalculated to include `ACCOUNT_STORAGE_OVERHEAD`. Validate the calculation against Solana CLI tools or official documentation to ensure alignment with Solana’s rent requirements.

## Patch

Resolved in PR#268 by hard-coding `MIN_DEPOSIT_LAMPORTS = 2_000_000`, which is sufficient to cover the rent for 49 bytes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Eclipse Canonical Bridge |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://www.eclipse.xyz/
- **GitHub**: https://github.com/Eclipse-Laboratories-Inc
- **Contest**: https://www.eclipse.xyz/

### Keywords for Search

`vulnerability`

