---
# Core Classification
protocol: Audit 507
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58347
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-05-blackhole
source_link: https://code4rena.com/reports/2025-05-blackhole
github_link: https://code4rena.com/audits/2025-05-blackhole/submissions/F-35

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - newspacexyz
---

## Vulnerability Title

[M-13] EIP-712 domain type hash mismatch breaks signature-based delegation

### Overview


The bug report is about a mistake in the code for the `VotingEscrow` contract. The constant `DOMAIN_TYPEHASH` is defined incorrectly and does not match how it is used in the contract. This can cause problems with signing and verifying messages, as well as breaking governance features that rely on off-chain signatures. To fix this issue, the `DOMAIN_TYPEHASH` should be updated to include the `version` field, which will ensure that the type hash matches the data structure used in the contract. This will fix the signature validation logic and prevent any further problems.

### Original Finding Content



<https://github.com/code-423n4/2025-05-blackhole/blob/92fff849d3b266e609e6d63478c4164d9f608e91/contracts/VotingEscrow.sol# L1205>

<https://github.com/code-423n4/2025-05-blackhole/blob/92fff849d3b266e609e6d63478c4164d9f608e91/contracts/VotingEscrow.sol# L1327-L1335>

### Finding description

There is a mistake in how the `DOMAIN_TYPEHASH` constant is defined and used in the `VotingEscrow` contract.
```

bytes32 public constant DOMAIN_TYPEHASH = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");
```

However, when building the domain separator, the contract includes an additional parameter:
```

bytes32 domainSeparator = keccak256(
    abi.encode(
        DOMAIN_TYPEHASH,
        keccak256(bytes(name)),
        keccak256(bytes(version)),
        block.chainid,
        address(this)
    )
);
```

The problem is that the `DOMAIN_TYPEHASH` does **not** include the `version` parameter, but the contract still tries to encode it. This creates a mismatch between the type hash and the actual encoding, which will lead to incorrect `digest` hashes when signing or verifying messages.

### Impact

* Users will be unable to sign or verify messages using the EIP-712 delegation feature.
* Delegation by signature (`delegateBySig`) will always fail due to signature mismatch.
* Governance features relying on off-chain signatures will break.

### Recommended mitigation steps

Update the `DOMAIN_TYPEHASH` to include the `version` field so that it matches the data structure used in the actual `domainSeparator`:
```

bytes32 public constant DOMAIN_TYPEHASH = keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)");
```

This change ensures the type hash includes all the fields being encoded and fixes the signature validation logic.

**Blackhole marked as informative**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Audit 507 |
| Report Date | N/A |
| Finders | newspacexyz |

### Source Links

- **Source**: https://code4rena.com/reports/2025-05-blackhole
- **GitHub**: https://code4rena.com/audits/2025-05-blackhole/submissions/F-35
- **Contest**: https://code4rena.com/reports/2025-05-blackhole

### Keywords for Search

`vulnerability`

