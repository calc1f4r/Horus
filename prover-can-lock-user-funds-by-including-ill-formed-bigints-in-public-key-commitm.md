---
# Core Classification
protocol: Succinct Labs Telepathy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21282
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
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
  - Joe Doyle
  - Marc Ilunga
  - Tjaden Hess
---

## Vulnerability Title

Prover can lock user funds by including ill-formed BigInts in public key commitment

### Overview


This bug report is about a data validation issue in the Rotate circuit of the circuits/circuits/rotate.circom. The circuit does not check the validity of BigInts included in pubkeysBigIntY. A malicious prover can exploit this vulnerability by carefully selecting malformed public keys and using the Rotate function, which will prevent future provers from using the default witness generator to make new proofs. This can lead to user funds being stuck in the bridge. Furthermore, invalid elliptic curve points can be used in the Step circuit, which can allow a malicious prover to forge Step proofs without a valid sync committee signature. 

The recommendation to fix this issue in the short term is to use a Num2Bits component to verify that each limb of the pubkeysBigIntY witness value is less than 2^55. In the long term, it is recommended to clearly document and validate the input assumptions of templates such as SubgroupCheckG1WithValidX. Additionally, the use of Circom signal tags can be considered to automate the checking of these assumptions.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Target: circuits/circuits/rotate.circom

## Description
The Rotate circuit does not check for the validity of BigInts included in `pubkeysBigIntY`. A malicious prover can lock user funds by carefully selecting malformed public keys and using the Rotate function, which will prevent future provers from using the default witness generator to make new proofs.

The Rotate circuit is designed to prove a translation between an SSZ commitment over a set of validator public keys produced by the Ethereum consensus protocol and a Poseidon commitment over an equivalent list. The SSZ commitment is over public keys serialized as 48-byte compressed BLS public keys, specifying an X coordinate and single sign bit, while the Poseidon commitment is over pairs (X, Y), where X and Y are 7-limb, 55-bit BigInts.

The prover specifies the Y coordinate for each public key as part of the witness; the Rotate circuit then uses `SubgroupCheckG1WithValidX` to constrain Y to be valid in the sense that (X, Y) is a point on the BLS12-381 elliptic curve. 

However, `SubgroupCheckG1WithValidX` assumes that its input is a properly formed BigInt, with all limbs less than `2^55`. This property is not validated anywhere in the Rotate circuit. By committing to a Poseidon root containing invalid BigInts, a malicious prover can prevent other provers from successfully proving a Step operation, bringing the light client to a halt and causing user funds to be stuck in the bridge. 

Furthermore, the invalid elliptic curve points would then be usable in the Step circuit, where they are passed without validation to the `EllipticCurveAddUnequal` function. The behavior of this function on ill-formed inputs is not specified and could allow a malicious prover to forge Step proofs without a valid sync committee signature. 

![Figure 1.1](https://placeholder.com) shows where the untrusted `pubkeysBigIntY` value is passed to the `SubgroupCheckG1WithValidX` template.

```
/* VERIFY THAT THE WITNESSED Y-COORDINATES MAKE THE PUBKEYS LAY ON THE CURVE */
component isValidPoint[SYNC_COMMITTEE_SIZE];
for (var i = 0; i < SYNC_COMMITTEE_SIZE; i++) {
  isValidPoint[i] = SubgroupCheckG1WithValidX(N, K);
  for (var j = 0; j < K; j++) {
    isValidPoint[i].in[0][j] <== pubkeysBigIntX[i][j];
    isValidPoint[i].in[1][j] <== pubkeysBigIntY[i][j];
  }
}
```

**Figure 1.1:** telepathy/circuits/circuits/rotate.circom#101–109

## Exploit Scenario
Alice, a malicious prover, uses a valid block header containing a sync committee update to generate a Rotate proof. Instead of using correctly formatted BigInts to represent the Y values of each public key point, she modifies the value by subtracting one from the most significant limb and adding `2^55` to the second-most significant limb. She then posts the resulting proof to the LightClient contract via the rotate function, which updates the sync committee commitment to Alice’s Poseidon commitment containing ill-formed Y coordinates. Future provers would then be unable to use the default witness generator to make new proofs, locking user funds in the bridge. Alice may be able to then exploit invalid assumptions in the Step circuit to forge Step proofs and steal bridge funds.

## Recommendations
- Short term, use a `Num2Bits` component to verify that each limb of the `pubkeysBigIntY` witness value is less than `2^55`.
- Long term, clearly document and validate the input assumptions of templates such as `SubgroupCheckG1WithValidX`. Consider adopting Circom signal tags to automate the checking of these assumptions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Succinct Labs Telepathy |
| Report Date | N/A |
| Finders | Joe Doyle, Marc Ilunga, Tjaden Hess |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-succinct-securityreview.pdf

### Keywords for Search

`vulnerability`

