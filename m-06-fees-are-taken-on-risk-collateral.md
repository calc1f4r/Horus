---
# Core Classification
protocol: Y2k Finance
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5787
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-y2k-finance-contest
source_link: https://code4rena.com/reports/2022-09-y2k-finance
github_link: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/44

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-06] Fees are taken on risk collateral

### Overview


This bug report focuses on a vulnerability in the Vault.sol code of the Y2K Finance project. It is found in lines 203-234 of the code, and the impact is that fees are taken on funds deposited as collateral. The proof of concept demonstrates how the fee is taken on the entire collateral deposited by the risk users. This is problematic for two reasons: it creates a disincentive for users to use the protocol, and it contradicts the project documents which state fees are only taken on the premiums and insurance payouts. The recommended mitigation step is to restructure the fee calculation, so it only takes fees on premiums and insurance payouts.

### Original Finding Content


Fees are taken on funds deposited as collateral.

### Proof of Concept

    uint256 feeValue = calculateWithdrawalFeeValue(entitledShares, id);

In L226 of Vault.sol#withdraw the fee is taken on the entire collateral deposited by the risk users. This is problematic for two reasons. The first is that the collateral provided by the risk users will likely be many many times higher than the premium being paid by the hedge users. This will create a strong disincentive to use the protocol because it is likely a large portion of the profits will be taken by fees and the risk user may unexpectedly lose funds overall if premiums are too low.

The second issue is that this method of fees directly contradicts project [documents](https://medium.com/@Y2KFinance/introducing-earthquake-pt-2-6f206cd4b315) which clearly indicate that fees are only taken on the premium and insurance payouts, not when risk users are receiving their collateral back.

### Recommended Mitigation Steps

Fee calculations should be restructured to only take fees on premiums and insurance payouts.

**[MiguelBits (Y2K Finance) disputed](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/44)**

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/44#issuecomment-1282077331):**
 > Agree with the warden. If the withdrawal fee exceeds the premium paid, risk users are disincentivised to provide collateral.  
> 
> > The second issue is that this method of fees directly contradicts project [documents](https://medium.com/@Y2KFinance/introducing-earthquake-pt-2-6f206cd4b315) which clearly indicate that fees are only taken on the premium and insurance payouts, not when risk users are receiving their collateral back.
> 
> Not sure if the warden is referring to the fee as the trading fee `c` in the article, but I would agree if it's the case. Implementation isn't according to spec. The actual fees charged might be more than expected.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Y2k Finance |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-y2k-finance
- **GitHub**: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/44
- **Contest**: https://code4rena.com/contests/2022-09-y2k-finance-contest

### Keywords for Search

`Business Logic`

