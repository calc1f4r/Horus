---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45344
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#1-unvalidated-variable-parameters-allow-fee-manipulation
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
  - MixBytes
---

## Vulnerability Title

Unvalidated Variable Parameters Allow Fee Manipulation

### Overview


The P2pLendingProxy contract has a bug in its deposit and withdraw functions that allows attackers to manipulate fees and bypass them. This happens because the contract does not properly check the parameters in the calldata passed to the lendingContract, which includes things like the asset, amount, and receiver. This can be exploited in various ways, such as inflating the amount deposited or specifying a different token than what is actually deposited. This bug is considered high severity because it can lead to significant financial losses for the protocol. To fix this, it is recommended to implement an adapter pattern for each lending protocol integration or expand the existing verification rules to check all non-static arguments.

### Original Finding Content

##### Description
This issue has been identified within the `deposit` and `withdraw` functions of the `P2pLendingProxy` contract. 

It is impossible to validate the variable parameters (such as `asset`, `amount`, or `receiver`) in the calldata passed to `lendingContract` under the current rule types (`StartsWith`, `EndsWith`). Attackers can exploit this lack of parameter integrity checks to manipulate fee calculations or bypass them entirely. 

For example: 
1. A user can call `deposit` with a larger token amount than what is actually deposited into the lending protocol, thus inflating `s_totalDeposited`. Later, they can redeem tokens from proxy balance via Permit2, creating a discrepancy between the protocol's recorded deposit and the actual tokens deposited, leading to fee bypassing. 
2. A user could specify a more valuable token (e.g., WETH) in the `deposit` function but actually deposit a cheaper one (e.g., USDC), causing `newProfit` to be undercounted and fees bypassed. 
3. A user can specify an arbitrary `receiver` address during withdrawal, avoiding the intended fee logic by redirecting tokens elsewhere. 
4. A user may pass one token as `vault` to the `withdraw` function but actually call `erc4626Redeem` on another token, again bypassing protocol fees.

These scenarios ultimately allow fee manipulation and value misreporting, resulting in potential financial losses to the protocol. 

This issue is classified as **high** severity because it enables direct fee manipulation and significant misreporting of asset flows.

##### Recommendation
We recommend implementing an adapter pattern for each lending protocol integration. This approach ensures all relevant parameters (`token`, `amount`, `receiver`, `vault`, etc.) are validated via a protocol-specific adapter rather than relying on general calldata verification rules alone. Alternatively, existing rule types could be expanded to verify all non-static arguments, though this might overcomplicate the verification logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#1-unvalidated-variable-parameters-allow-fee-manipulation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

