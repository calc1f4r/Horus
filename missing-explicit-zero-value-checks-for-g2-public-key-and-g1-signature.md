---
# Core Classification
protocol: Symbiotic Key Registry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64220
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-key-registry-v2.0.md
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
finders_count: 4
finders:
  - Alex Roan
  - 0kage
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Missing Explicit Zero-Value Checks for G2 Public Key and G1 Signature

### Overview

See description below for full details.

### Original Finding Content

**Description:** The BLS12381 verification logic explicitly rejects a zero G1 public key, but does not explicitly reject
1) a zero G2 public key, or
2) a zero G1 signature.

```solidity
/**
 * @notice Verify a BLS signature.
 * @param keyG1 The G1 public key.
 * @param messageHash The message hash to verify.
 * @param signatureG1 The G1 signature.
 * @param keyG2 The G2 public key.
 * @return If the signature is valid.
 * @dev Burns the whole gas if pairing precompile fails.
 *      Returns false if the key is zero G1 point.
 */
function verify(
    BLS12381.G1Point memory keyG1,
    bytes32 messageHash,
    BLS12381.G1Point memory signatureG1,
    BLS12381.G2Point memory keyG2
) internal view returns (bool) {
    if (keyG1.x_a == 0 && keyG1.x_b == 0 && keyG1.y_a == 0 && keyG1.y_b == 0) {
        return false;
    }
    BLS12381.G1Point memory messageG1 = BLS12381.hashToG1(abi.encodePacked(messageHash));
    uint256 alpha = uint256(keccak256(abi.encode(signatureG1, keyG1, keyG2, messageG1))) % BLS12381.FR_MODULUS;

    return BLS12381.pairing(
        signatureG1.add(keyG1.scalarMul(alpha)),
        BLS12381.negGeneratorG2(),
        messageG1.add(BLS12381.generatorG1().scalarMul(alpha)),
        keyG2
    );
}
```

While these cases are not exploitable in practice due to the behavior of the BLS12-381 precompiles (which prevent malformed curve points from passing pairing checks), zero-valued keys and signatures are not valid inputs in the BLS specification and should be rejected for clarity and consistency.

Allowing zero G2 keys introduces a degenerate verification path where the second pairing term collapses to the identity. Zero signatures are similarly invalid from a protocol-design perspective and should be excluded explicitly to avoid ambiguity for integrators and future code maintainers.

**Recommended Mitigation:** Add explicit zero checks before invoking any curve or pairing operations, notably the G2 public key and G1 signature.

**Symbiotic:** Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic Key Registry |
| Report Date | N/A |
| Finders | Alex Roan, 0kage, Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-key-registry-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

