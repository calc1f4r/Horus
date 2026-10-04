---
# Core Classification
protocol: XDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61885
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
source_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - István Böhm
  - Andy Lin
  - Cameron Biniamow
---

## Vulnerability Title

Abrupt Fee Jump in `_calculate_service_fee()` Leads to Unpredictable Costs

### Overview


This bug report describes a problem with the `_calculate_service_fee()` function in the `factory` contract. The function is used to determine the deployment fees for new contracts, but it has a misconfigured threshold that causes a sudden drop in fees from 1200 TON to 25 TON. This can confuse users and be exploited by timing contract creations around the threshold. The team has recommended a new, multi-tiered fee structure that includes a fixed fee of 25 TON for contracts created after the 500,000th one. They have also provided code for a corrected implementation of the function.

### Original Finding Content

**Update**
The team fixed the issue as recommended. Addressed in: `7770391d2049df53b6ba40f4e564103c04f7970e`.

**File(s) affected:**`contracts/factory.fc`

**Description:** The `_calculate_service_fee()` function in `factory` determines deployment fees based on `data::count`. Its conditional thresholds cause a sharp and counterintuitive fee drop from over 1200 TON at `count = 500_000` to 25 TON at `count = 500_001`, likely due to a misconfigured threshold. Such unpredictable jumps can confuse users and be exploited by timing contract creations around the boundary.

After consulting with the team, we get the expected logic to be a multi-tiered, linear progressive fee:

*   1st DAO: 0.1 TON.
*   1st to 1,000th DAO: A linear increase from 0.1 TON to 2.5 TON.
*   1,001st to 500,000th DAO: A linear increase from 2.5 TON to 25 TON.
*   500,001st DAO onwards: A fixed fee of 25 TON.

**Exploit Scenario:**

1.   An attacker waits until `data::count` is one above the threshold (e.g., 500 001).
2.   They deploy a DAO at the lower 25 TON fee instead of the expected 1 200 TON, gaining a large cost advantage.
3.   Conversely, users could be overcharged if they deploy just before the threshold.

**Recommendation:** Replace the current `_calculate_service_fee()` function with a corrected implementation that accurately reflects the intended multi-tiered, progressive fee structure. The following code correctly calculates the fee at each stage:

```
int _calculate_service_fee() impure {
    if (data::count > 500000) {
        return 25 * NANO; ;; 25 TON - fixed fee
    }

    if (data::count <= 1) {
        return NANO / 10; ;; 0.1 TON for the first DAO
    }

    if (data::count <= 1000) {
        ;; Linear progression from 0.1 TON (DAO 1) to 2.5 TON (DAO 1000)
        int base_fee = NANO / 10; ;; 0.1 TON
        int total_increase = 25 * NANO / 10 - base_fee; ;; 2.4 TON
        int fee_increase = (data::count - 1) * total_increase / 999;
        return base_fee + fee_increase;
    }

    ;; data::count > 1000 and data::count <= 500000
    ;; Linear progression from 2.5 TON (at DAO 1000) to 25 TON (at DAO 500,000)
    int base_fee = 25 * NANO / 10; ;; 2.5 TON
    int total_increase = 25 * NANO - base_fee; ;; 22.5 TON
    int fee_increase = (data::count - 1000) * total_increase / (500000 - 1000);
    return base_fee + fee_increase;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | XDAO |
| Report Date | N/A |
| Finders | István Böhm, Andy Lin, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html

### Keywords for Search

`vulnerability`

