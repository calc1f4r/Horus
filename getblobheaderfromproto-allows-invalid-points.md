---
# Core Classification
protocol: EigenDA vCISO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61699
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Eigenlayer-Spearbit-vCISO-February-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Eigenlayer-Spearbit-vCISO-February-2025.pdf
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

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - DTheo
  - Justin Traglia
---

## Vulnerability Title

GetBlobHeaderFromProto allows invalid points

### Overview


This report highlights a high risk vulnerability in the `utils.go` file of the `node/grpc` module. The vulnerability is caused by manually setting the components/limbs of certain points without checking if they are valid. This can potentially impact pairing checks and may lead to security issues. The report recommends either casting the values to `bn254.G*Affine` and performing checks, or using compressed serialization and `bn254.G*Affine#SetBytes` to address this issue. 

### Original Finding Content

## High Risk Vulnerability Report

## Severity
**High Risk**

## Context
- `node/grpc/utils.go#L65-L66`
- `node/grpc/utils.go#L73-L76`
- `node/grpc/utils.go#L79-L82`

## Description
In `GetBlobHeaderFromProto`, the components/limbs (X, Y) of the points (Commitment, LengthCommitment, and LengthProof) are manually set. Doing it this way will not check if the point is valid (on the curve, in the right subgroup, etc). This may actually impact pairing checks. Eventually, this point is casted to `abn254.G1Affine` which won't check if the point is valid either.

Also, just a little nit, `h.GetLengthCommitment() != nil` and `h.GetLengthProof() != nil` checks are unnecessary as protobuf getter functions are guaranteed not to return nil.

## Recommendation
Either of the following:
1. In `GetBlobHeaderFromProto`, cast the values to `bn254.G*Affine` and call `p.IsOnCurve()` and `p.IsInSubGroup()`.
2. Use compressed serialization and `bn254.G*Affine#SetBytes` which performs these checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | EigenDA vCISO |
| Report Date | N/A |
| Finders | DTheo, Justin Traglia |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Eigenlayer-Spearbit-vCISO-February-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Eigenlayer-Spearbit-vCISO-February-2025.pdf

### Keywords for Search

`vulnerability`

