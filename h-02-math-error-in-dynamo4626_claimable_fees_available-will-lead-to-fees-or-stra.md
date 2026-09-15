---
# Core Classification
protocol: Dynamo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55645
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
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
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[H-02] Math error in Dynamo4626#\_claimable_fees_available will lead to fees or strategy lockup

### Overview


The bug report is about an issue in the code that calculates fees for a financial platform called Dynamo Finance. The problem occurs when trying to claim fees for the "proposer" type, which results in the function unexpectedly reverting and causing fees to become stuck. This is because the assert statement in the code always compares the total fees to be claimed as if it were for both proposer and yield fees, instead of just the proposer fees. The recommendation is to fix this by checking the appropriate values for each type of fee. The issue has been remedied by splitting the fee calculations based on the type of fee being claimed.

### Original Finding Content

**Details**

[Dynamo4626.vy#L428-L438](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L428-L438)

    fee_percentage: uint256 = YIELD_FEE_PERCENTAGE
    if _yield == FeeType.PROPOSER:
        fee_percentage = PROPOSER_FEE_PERCENTAGE
    elif _yield == FeeType.BOTH:
        fee_percentage += PROPOSER_FEE_PERCENTAGE
    elif _yield != FeeType.YIELD:
        assert False, "Invalid FeeType!"

    total_fees_ever : uint256 = (convert(total_returns,uint256) * fee_percentage) / 100

    assert self.total_strategy_fees_claimed + self.total_yield_fees_claimed <= total_fees_ever, "Total fee calc error!"

In the assert statement, total_fees_ever is compared against both fees types of fees claimed. The issue with this is that this is a relative value depending on which type of fee is being claimed. The assert statement on the other hand always compares as if it is FeeType.BOTH. This will lead to this function unexpectedly reverting when trying to claim proposer fees. This leads to stuck fees but also proposer locked as described in H-01.

**Lines of Code**

[Dynamo4626.vy#L418-L459](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L418-L459)

**Recommendation**

Check should be made against the appropriate values (i.e. proposer should be check against only self.total_strategy_fees_claimed).

**Remediation**

Fixed [here](https://github.com/DynamoFinance/vault/commit/6e762711f55f9cf4bece42706ddef7c92d5b4ac4) and [here](https://github.com/DynamoFinance/vault/commit/c649ceda1b7b15b14486bd1332aefb8d48ed5279) by splitting fee calculations base on fee type being claimed

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Dynamo |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

