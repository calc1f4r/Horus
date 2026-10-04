---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53483
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[LID-24] Withdrawal Queue ERC721 ownerOf gas optimisation

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** WithdrawalQueueERC721.sol:ownerOf#L156-L163

**Description:**

In the `ownerOf` function, the `WithdrawalRequest` of the corresponding `requestId` is retrieved. The request is loaded fully into memory and both storage slots will be loaded.

However, only the values `claimed` and `owner` are used, which are both in the second slot only. Therefore, by replacing `WithdrawalRequest memory` with `WithdrawalRequest` storage on line 159, one `SLOAD` can be saved on each call.
```
function ownerOf(uint256 _requestId) public view override returns (address) {
    if (_requestId == 0 || _requestId > getLastRequestId()) revert InvalidRequestId(_requestId);

    WithdrawalRequest memory request = _getQueue()[_requestId];
    if (request.claimed) revert RequestAlreadyClaimed(_requestId);

    return request.owner;
}
```

**Remediation:**  We would recommend to apply the optimisation as shown in the description, in favour of gas optimisation.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

