---
# Core Classification
protocol: Mellow Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1154
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-mellow-protocol-contest
source_link: https://code4rena.com/reports/2021-12-mellow
github_link: https://github.com/code-423n4/2021-12-mellow-findings/issues/44

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
  - services
  - yield_aggregator
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-07] Bad redirects can make it impossible to deposit & withdraw

### Overview


A bug has been identified in the `GatewayVault._push()` function of the GatewayVault smart contract. This function gets `redirects` from the `strategyParams` and if `redirects[i] = j`, vault index `i`'s deposits are redirected to vault index `j`. When this happens, the deposits for vault index `i` are cleared. The same is true for withdrawals in the `_pull` function. This could mean users are unable to withdraw.

The bug occurs when the `redirects` array is misconfigured. For example, if `0` redirects to `1` and `1` redirects to `0`. Or `0` redirects to itself, etc. In this case, all `amountsByVault` are set to zero, meaning users are unable to deposit to the pool.

The recommended mitigation steps to prevent this bug from occurring are to restrict the `redirects[i] = j` matrix. If `i` is redirected to `j`, `j` may not redirect itself. This should be checked when setting the `redirects` array.

### Original Finding Content

_Submitted by cmichel_

The `GatewayVault._push()` function gets `redirects` from the `strategyParams`.
If `redirects[i] = j`, vault index `i`'s deposits are redirected to vault index `j`.

Note that the deposits for vault index `i` are cleared, as they are redirected:

```solidity
for (uint256 j = 0; j < _vaultTokens.length; j++) {
    uint256 vaultIndex = _subvaultNftsIndex[strategyParams.redirects[i]];
    amountsByVault[vaultIndex][j] += amountsByVault[i][j];
    amountsByVault[i][j] = 0;
}
```

> The same is true for withdrawals in the `_pull` function. Users might not be able to withdraw this way.

If the `redirects` array is misconfigured, it's possible that all `amountsByVault` are set to zero.
For example, if `0` redirects to `1` and `1` redirects to `0`. Or `0` redirects to itself, etc.
There are many misconfigurations that can lead to not being able to deposit to the pool anymore.

#### Recommended Mitigation Steps

The `redirects[i] = j` matrix needs to be restricted.
If `i` is redirected to `j`, `j` may not redirect itself.
Check for this when setting the `redirects` array.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-12-mellow-findings/issues/44#issuecomment-1005680123):**
 > Can you confirm if this issue is valid or not? @MihanixA 

**[MihanixA (Mellow Protocol) confirmed](https://github.com/code-423n4/2021-12-mellow-findings/issues/44#issuecomment-1006406574):**
 > @0xleastwood Confirmed

**[MihanixA (Mellow Protocol) commented](https://github.com/code-423n4/2021-12-mellow-findings/issues/44#issuecomment-1006407377):**
 > (notice that this one is a deploy-related issue)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mellow Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-mellow
- **GitHub**: https://github.com/code-423n4/2021-12-mellow-findings/issues/44
- **Contest**: https://code4rena.com/contests/2021-12-mellow-protocol-contest

### Keywords for Search

`vulnerability`

