---
# Core Classification
protocol: Venus Income Allocation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60381
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
source_link: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
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
  - Shih-Hung Wang
  - Nikita Belenkov
  - Michael Boyle
  - Mostafa Yassin
---

## Vulnerability Title

Potential Limitation in `VBNBAdmin` Design

### Overview

See description below for full details.

### Original Finding Content

**Update**
The client has acknowledged the issue and commented: "The vBNBAdmin has no such scenarios where it needs to receive BNB that doesn't need to go to the ProtocolShareReserve contract. The fallback can only be triggered via owner and owner is timelock there (this function is called via Governance process always)".

**File(s) affected:**`contracts/Admin/VBNBAdmin.sol`

**Description:** The `VBNBAdmin` contract implements a `fallback()` function that is only callable by the admin, and this function forwards the call to the `vBNB` contract. This design allows the admin to call any function on the `vBNB` contract as needed.

However, if the call to the `vBNB` contract results in a BNB transfer back to the `VBNBAdmin` contract, no mechanism is currently in place to retrieve the received BNB specifically. These BNB will be considered token reserves and forwarded to the `ProtocolShareReserve` contract when the `reduceReserves()` is called.

**Recommendation:** Confirm whether this is an intended design. If so, consider updating the internal documentation to clarify the limitations and potential consequences of using the `VBNBAdmin` contract. If it is not intentional and there is a need to retrieve the received BNB separately, consider implementing the necessary functionality to achieve this.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Income Allocation |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Michael Boyle, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html

### Keywords for Search

`vulnerability`

