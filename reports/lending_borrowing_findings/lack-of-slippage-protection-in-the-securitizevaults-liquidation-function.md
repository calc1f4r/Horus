---
# Core Classification
protocol: Securitize Redeem Swap Vault Na
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64246
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
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
finders_count: 1
finders:
  - Hans
---

## Vulnerability Title

Lack of slippage protection in the SecuritizeVault's liquidation function

### Overview


A bug has been found in the `liquidate()` function of SecuritizeVault. This function converts share tokens to asset tokens, but does not allow users to specify a minimum output amount. This means that users may receive fewer assets than expected, leading to financial losses. To fix this issue, it is recommended to add a `minOutputAmount` parameter to the function, implement a time limit, and add events for monitoring purposes. This bug has been fixed in the latest commit and verified by Cyfrin. 

### Original Finding Content

**Description:** The SecuritizeVault's `liquidate()` function converts share tokens to asset tokens using the NAV provider's rate without allowing users to specify a minimum output amount. Since the conversion rate is dynamic and external redemption may be involved, users are exposed to potential value loss from rate changes between transaction submission and execution. This is particularly concerning in volatile market conditions or when there is high latency in transaction processing.

**Impact:** Users may receive fewer assets than expected during liquidation due to rate changes, leading to direct financial losses.

**Recommended Mitigation:**
1. Add a `minOutputAmount` parameter to the liquidate function:
```solidity
function liquidate(uint256 shares, uint256 minOutputAmount) public override(ISecuritizeVault) whenNotPaused {
...
    require(assets >= minOutputAmount, "Insufficient output amount");
...
}
```
2. Consider implementing a time limit parameter to protect against long-pending transactions
3. Add events to track actual output amounts for monitoring purposes

**Securitize:** Fixed in commit [42e651](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/42e6511931f03b266b3acd4ca220544246efb4ab).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Redeem Swap Vault Na |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

