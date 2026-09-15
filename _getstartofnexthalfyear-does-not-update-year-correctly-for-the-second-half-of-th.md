---
# Core Classification
protocol: Huma Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35892
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - 0xLeastwood
  - Saw-Mon and Natalie
  - Jonatas Martins
  - Kankodu
---

## Vulnerability Title

_getStartOfNextHalfYear does not update year correctly for the second half of the year

### Overview


The bug report describes a problem in the code for a calendar feature in a program. The issue is that the year is not being incremented correctly when calculating the start of the next half year. The recommended solution is to make changes to the code and add more test cases. The severity of the bug is high, but it is not expected to affect real-life scenarios. The bug has been fixed in a pull request.

### Original Finding Content

## Severity: High Risk

## Context
`Calendar.sol#L208`

## Description
The `year` is not incremented for the second half of the year when calculating the `startOfNextHalfYear`:

```solidity
(uint256 year, uint256 month, ) = DTL.timestampToDate(timestamp);
startOfNextHalfYear = DTL.timestampFromDate(year, month > 6 ? 1 : 7, 1);
```

If `month > 6` is true, one should also increment the `year`.

## Recommendation
Instead, one should do:

```solidity
function _getStartOfNextHalfYear(
    uint256 timestamp
) internal pure returns (uint256 startOfNextHalfYear) {
    (uint256 year, uint256 month, ) = DTL.timestampToDate(timestamp);
    if (month > 6) {
        month = 1;
        ++year;
    } else {
        month = 7;
    }
    startOfNextHalfYear = DTL.timestampFromDate(year, month, 1);
}
```

Additionally, unit test cases are missing that check this condition. At least two more test cases need to be added. Here is one by providing a `0` timestamp:

```diff
diff --git a/test/unit/common/CalendarTest.ts b/test/unit/common/CalendarTest.ts
index 4fbcd4d..1cd0bbb 100644
--- a/test/unit/common/CalendarTest.ts
+++ b/test/unit/common/CalendarTest.ts
@@ -782,6 +782,28 @@ describe("Calendar Test", function () {
),
).to.equal(startDateOfNextPeriod.unix());
});
+
+ it("Should return the start date of the immediate next period relative to the current block timestamp if timestamp is 0 and the next period is in the next year", async function () {
+ const nextYear = moment.utc().year() + 1;
+ const nextBlockTime = moment.utc({
+ year: nextYear,
+ month: 10,
+ day: 2,
+ });
+ await mineNextBlockWithTimestamp(nextBlockTime.unix());
+
+ const startDateOfNextPeriod = moment.utc({
+ year: nextYear + 1,
+ month: 0,
+ day: 1,
+ });
+ expect(
+ await calendarContract.getStartDateOfNextPeriod(
+ PayPeriodDuration.SemiAnnually,
+ 0,
+ ),
+ ).to.equal(startDateOfNextPeriod.unix());
+ });
});
});
```

## Run
Run the following command to execute the tests:
```bash
yarn hardhat test --network hardhat --grep "Calendar Test"
```

## Note
**Huma**: Good catch, this is a bug that we will fix; however, the severity should not be high risk since we do not expect this function to be called in real life, thus posing an extremely low likelihood. Since we focus on short-duration loans, no period will be longer than one month. This semi-annual period feature is added purely for future expansion. Fixed in PR 403.

**Spearbit**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Huma Finance |
| Report Date | N/A |
| Finders | 0xLeastwood, Saw-Mon and Natalie, Jonatas Martins, Kankodu |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

