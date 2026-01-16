---
# Core Classification
protocol: Teahouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45704
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Arbitrary Address Supplied to executeSwap of the TeaVaultAmbient Contract Allows the Pool Manager to Drain the Pool Resulting in a Theft of Funds

### Overview


This bug report discusses a vulnerability in the TeaVaultAmbient contract, which is used to manage funds on the Ambient swap dex. The executeSwap function in this contract can be manipulated by a malicious contract, allowing the pool manager to extract funds at a lower rate than the market value. This has already been demonstrated with a proof of concept, where the attacker was able to steal over $23,000 worth of ETH. The recommendation to fix this issue is to restrict the _swapRouter parameter to a whitelist of trusted addresses and implement strict validation on swap data. It is also suggested to integrate with well-known and audited decentralized exchanges to prevent further misuse. 

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Location**: TeaVaultAmbient.sol#executeSwap

**Description**: 

The TeaVaultAmbient contract is a wrapper around the Ambient swap dex which allows funds to be deposited by users where these funds are managed by the pool manager actor who has the authority to add liquidity to a strategy and perform swaps on behalf of the user. The executeSwap function allows the pool manager to execute a swap from any router via the swap relayer. This function takes an address (swap router), however, the address supplied to the function can be a malicious contract which will allow the pool manager to extract funds from the contract by paying well under market rates bypassing the validation against baselineValue. 
Consider the proof of concept secret gist below where a user deposits ETH into the contract and the pool manager proceeds to extract $23,577 USD (at the time of writing) worth of ETH in exchange for ~$5,000 DAI:
https://gist.github.com/chris-zokyo/0458e8bf019f1143211322b937a3aee6 
A flashloan may allow the attacker to steal funds from vaults with significantly more value. 

**Recommendation**

Restrict the _swapRouter parameter to a whitelist of trusted and verified swap router addresses in the form of a mapping set by protocol admins. In addition to this, implement strict validation on the swap data and consider integrating with well-known and audited decentralized exchanges (DEXs) to prevent misuse.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Teahouse |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

