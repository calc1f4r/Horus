---
# Core Classification
protocol: Autograph
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48200
audit_firm: OtterSec
contest_link: https://autograph.io
source_link: https://autograph.io
github_link: https://github.com/Autograph-Core/Smart-Contracts-Audit-Repo

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
  - Akash Gurugunti
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Improper Implementation Of VRF Requesting

### Overview


The bug report is about a problem in the VRFv2Consumer.sol file where the function requestRandomWords is used to request a list of random words from the Chainlink VRF Coordinator. However, the current implementation does not check for any pending requests before sending a new one, which can result in overwriting variables and unexpected behaviors. This was demonstrated in a scenario where two requests were made, but the response for the first request was used for the second request, causing all participants to be selected as winners. The suggested solution is to validate the current pending request and reset variables after consuming the random words. This bug has been fixed in the latest version.

### Original Finding Content

## Overview

In `VRFv2Consumer.sol`, `requestRandomWords` is used to request a list of random words from the Chainlink VRF Coordinator. This function should only be called when there are no pending requests that need to be fulfilled. The `currentRNGName` and `s_requestId` variables are used to store the name and ID of the current pending requests.

## Issue

The current implementation does not check if there is a pending request before sending a new request. This results in overwriting the `currentRNGName` and `s_requestId` variables. As a result, a response to the past request may be fulfilled as a response to the current pending request, which may lead to unexpected behaviors.

## Proof of Concept

Consider the following scenario:

1. A request (`request1`) has been raised by calling `requestRandomWords`, requesting random words to select five winners from a list of 20 participants.
2. Another request (`request2`) has been raised while the first request is still pending, requesting random words to select three winners from a list of five participants.
3. The response for the first request is fulfilled, while the second request is considered the current pending request.
4. Since the `requestId` is not validated in `fulfillRandomWords`, the `randomWords` of length five is used to calculate winners from the list of five participants, resulting in all participants becoming the winners.

## Remediation

- Validate whether the name and ID of the current pending request, such as `currentRNGName` and `s_requestId`, have zero values before sending the request in `requestRandomWords`.
- Additionally, set these variables to zero values after consuming the `randomWords` in `fulfillRandomWords`.
- Also, validate whether the `requestId` parameter is equal to the `s_requestId` in `fulfillRandomWords`.

## Patch

Fixed in commit `8004a0c`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Autograph |
| Report Date | N/A |
| Finders | Akash Gurugunti, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://autograph.io
- **GitHub**: https://github.com/Autograph-Core/Smart-Contracts-Audit-Repo
- **Contest**: https://autograph.io

### Keywords for Search

`vulnerability`

