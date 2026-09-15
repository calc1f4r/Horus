---
# Core Classification
protocol: Growth Defi V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13576
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/12/growth-defi-v1/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - John Mardlin
  - Alexander Wade
---

## Vulnerability Title

Potential resource exhaustion by external calls performed within an unbounded loop

### Overview


This bug report is about the `DydxFlashLoanAbstraction._requestFlashLoan` function, which is part of the code in the file `DydxFlashLoanAbstraction.sol` on line 62 to 69. This function performs external calls in a potentially-unbounded loop. Depending on changes made to DyDx’s `SoloMargin`, this could make the flash loan provider too expensive, or in the worst case, impossible to execute due to the block gas limit. This bug report is important because it could cause problems with the code if changes are made to the `SoloMargin` and the code is not updated accordingly.

### Original Finding Content

#### Description


`DydxFlashLoanAbstraction._requestFlashLoan` performs external calls in a potentially-unbounded loop. Depending on changes made to DyDx’s `SoloMargin`, this may render this flash loan provider prohibitively expensive. In the worst case, changes to `SoloMargin` could make it impossible to execute this code due to the block gas limit.


**code/contracts/modules/DydxFlashLoanAbstraction.sol:L62-L69**



```
uint256 \_numMarkets = SoloMargin(\_solo).getNumMarkets();
for (uint256 \_i = 0; \_i < \_numMarkets; \_i++) {
	address \_address = SoloMargin(\_solo).getMarketTokenAddress(\_i);
	if (\_address == \_token) {
		\_marketId = \_i;
		break;
	}
}

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Growth Defi V1 |
| Report Date | N/A |
| Finders | John Mardlin, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/12/growth-defi-v1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

