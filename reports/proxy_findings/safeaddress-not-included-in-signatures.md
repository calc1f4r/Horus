---
# Core Classification
protocol: Parcel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54847
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a
source_link: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
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
finders_count: 3
finders:
  - Christos Pap
  - Krum Pashov
  - Gerard Persoon
---

## Vulnerability Title

safeAddress not included in signatures 

### Overview


This bug report highlights a security issue in the PayrollManager smart contract. The issue arises due to the validation of signatures not taking into account the safeAddress, which can lead to the reuse of signatures from the same approvers who are involved in other organizations/sub DAOs/safes. This can result in the theft of ETH or tokens. 

The code example provided shows that the nonces used for payment can be reused, combined with another issue, making it possible for attackers to steal funds. The recommendation is to include the safeAddress in the signatures to prevent this issue. 

The report also mentions that the issue can be solved by using the Proxy Pattern and that the `DomainSeparator` now contains `address(this)` to prevent mixing signatures from multiple Gnosis safes.

### Original Finding Content

## Security Issue in PayrollManager

## Context
- `PayrollManager.sol#L139-L244`
- `PayrollManager.sol#L104-L124`
- `Signature.sol#L39-L52`

## Description
The validation of signatures doesn’t take into account the `safeAddress` (except when checking the number of approvals). This means signatures from the same approvers who are also involved in other organizations/sub DAOs/safes could be reused. As the nonces (e.g. `packPayoutNonce()`) are stored in a different storage location, the nonces can be reused and thus the payment can be done again. Combined with the issue "More tokens can be retrieved from a safe via frontrunning", this means ETH/Tokens can be stolen.

### Code Example
```solidity
function executePayroll(...) ... {
    ...
    validateSignatures(safeAddress, roots, signatures);
    ...
    bytes32 leaf = encodeTransactionData(to[i], tokenAddress[i], amount[i], payoutNonce[i]);
    ...
    if (MerkleProof.verify(proof[i][j], roots[j], leaf)) {
        ++approvals;
    }
    if (approvals >= orgs[safeAddress].approvalsRequired && ... ) {
        ...
    }
    ...
}
```

```solidity
function validateSignatures(...) ... {
    ...
    address signer = validatePayrollTxHashes(roots[i], signatures[i]);
    ...
}
```

```solidity
function validatePayrollTxHashes(...) ... {
    bytes32 digest = ... abi.encode(PAYROLL_TX_TYPEHASH, rootHash) ...
    return digest.recover(signature);
}
```

## Recommendation
Include the `safeAddress` in the signatures, for example in the following way:

```solidity
function validatePayrollTxHashes(...) ... {
    - bytes32 digest = ... abi.encode(PAYROLL_TX_TYPEHASH, rootHash) ...
    + bytes32 digest = ... abi.encode(PAYROLL_TX_TYPEHASH, safeAddress, rootHash) ...
    return digest.recover(signature);
}
```

**Note:** The recommendation of the issue "Use separate contracts for each Gnosis safe" also solves this issue, but having a signed `safeAddress` is always safer.

## Parcel
This is solved by using the Proxy Pattern.

## Cantina Security
The `DomainSeparator` contains `address(this)` so signatures from multiple Gnosis safes can no longer be mixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Parcel |
| Report Date | N/A |
| Finders | Christos Pap, Krum Pashov, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a

### Keywords for Search

`vulnerability`

