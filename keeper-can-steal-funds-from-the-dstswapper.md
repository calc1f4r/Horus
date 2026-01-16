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
solodit_id: 40854
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
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

Keeper can steal funds from the dstswapper 

### Overview


This bug report discusses a potential issue with a function called DstSwapper.processTx, which is responsible for swapping tokens when a user deposits to another chain. The report explains that a malicious keeper could exploit this function by creating a small deposit with a high slippage and then swapping the entire balance of the interim token in order to steal the user's funds. The report recommends implementing oracles to calculate the approximate value of the tokens and limiting the amount that a keeper can use in the other asset to prevent this type of exploit. 

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Proof of Concept
When a user deposits to another chain, they can perform a DST swap, meaning that after bridging from the source to the destination, the bridge won't send the vault's asset to the destination chain. This interim token should be swapped for the vault's asset, which is handled by keepers calling the `DstSwapper.processTx` function and providing the swapping `txData`, containing information about the swap.

All validation and swaps occur inside `_processTx`. The token and amount to be sent are decoded from `txData`, and it is checked that the token is the same as the user's interim token. Following this, `txData` is validated to ensure that the receiver of the swap is set to the CSR. Upon successful validation, the swap is executed. In the end, a check confirms that the CSR indeed has increased its balance by the amount that the user has requested.

Currently, keepers belong to the protocol; however, there are plans to change this and allow other entities to execute that role.

A malicious keeper could create a small deposit from one chain to another with a DST swap and set the interim token to the one they intend to steal. In this deposit, they can provide high slippage (greater than 90) to sandwich the subsequent swap (which swaps the entire balance of the interim token in the `DstSwapper`), parameterized in the provided `txData`, in order to profit from the high slippage and large amount of tokens. As a result, after the swap, a certain amount of tokens will still be sent to the CSR, which explains why the balance and slippage checks pass and the transaction does not revert, while enabling the malicious keeper to steal the user's funds from the `DstSwapper`.

## Recommendation
Consider implementing some kind of oracles to calculate the approximate value of the tokens that the depositor expects to receive, and then disallow the keeper from using more than that value in the other asset, with some allowable deviation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

