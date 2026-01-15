---
# Core Classification
protocol: Secured Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59982
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
source_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
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
  - Mustafa Hasan
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

The Emergency Termination Mechanism Can Be Negatively Impacted by Incorrect Prices Sent by the Oracle

### Overview


This bug report discusses a potential issue with the emergency termination mechanism in the LendingMarketController contract. The client has provided a solution using mock price feed contracts, but there are concerns that this may not fully solve the problem if the emergency is caused by incorrect prices from the oracle. The recommendation is to further improve the emergency termination mechanism to address this issue.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> _We have mock price feed contracts which return the fixed price. These contracts inherit the interface of the Chainlink Price Feed contract. Therefore, we can use our mock price feed instead of the Chainlink Price Feed contract when something happens. We use these mock contracts to solve this issue by the following steps:_
> 
> 
> 1.   _Pause all order books._
> 2.   _Replace price feeds that return incorrect prices with mock price feeds._
> 3.   _Execute emergency termination._

**File(s) affected:**`LendingMarketOperationLogic.sol`

**Description:** In case of an emergency, a termination mechanism can be executed by the owner of the contract `LendingMarketController` to cease the operations of the protocol. Once executed, this operation cannot be reverted.

For each active currency, the last aggregated price returned by the oracle is stored in the mapping `marketTerminationPrices`. Then, users can force a settlement of all their lending and borrowing positions via the function `executeEmergencySettlement()`.

However, if the emergency is caused by incorrect prices returned by the oracle, these prices will be recorded as reference prices and it would negatively impact the settlement phase as the coverage calculation would provide incorrect values.

**Recommendation:** Consider adapting the emergency termination mechanism to mitigate/eliminate the impact of incorrect prices provided by the oracle.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Secured Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html

### Keywords for Search

`vulnerability`

