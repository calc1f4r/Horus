---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25359
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-07-axelar
source_link: https://code4rena.com/reports/2022-07-axelar
github_link: https://github.com/code-423n4/2022-07-axelar-findings/issues/20

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
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] System will not work anymore after EIP-4758

### Overview


This bug report is about the deposit service of the Axelar application. The deposit service will no longer work due to the upcoming Ethereum Improvement Proposal (EIP) 4758, which will remove the `SELFDESTRUCT` opcode. This means that the current deposit system will no longer work. To avoid this, the architecture of the deposit service should be changed, so users can interact directly with the deposit service, which will keep track of funds and provide refunds directly. The severity of the bug was acknowledged by re1ro (Axelar) and Alex the Entreprenerd (judge) and was determined to be of medium severity, as the fork is not in place yet and there is no clear timeline for its implementation.

### Original Finding Content

_Submitted by Lambda, also found by Chom_

[DepositReceiver.sol#L25](https://github.com/code-423n4/2022-07-axelar/blob/a46fa61e73dd0f3469c0263bc6818e682d62fb5f/contracts/deposit-service/DepositReceiver.sol#L25)<br>

After [EIP-4758](https://eips.ethereum.org/EIPS/eip-4758), the `SELFDESTRUCT` op code will no longer be available. According to the EIP, "The only use that breaks is where a contract is re-created at the same address using CREATE2 (after a SELFDESTRUCT)". Axelar is exactly such an application, the current deposit system will no longer work.

### Recommended Mitigation Steps

To avoid that Axelar simply stops working one day, the architecture should be changed. Instead of generating addresses for every user, the user could directly interact with the deposit service and the deposit service would need to keep track of funds and provide refunds directly.

**[re1ro (Axelar) commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/20#issuecomment-1205926507):**
 > Very good spot. We will address this.

**[re1ro (Axelar) acknowledged](https://github.com/code-423n4/2022-07-axelar-findings/issues/20)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/20#issuecomment-1236399840):**
 > The warden has shown a plausible upgrade path for Ethereum that will remove the `SELFDESTRUCT` opcode, bricking the `DepositReceiver` functionality.
> 
> If the fork was in place today, the code would be broken, and the finding should be of high severity.
> 
> Because the fork is not in place, and no clear timeline is defined for "The Purge", I think Medium Severity to be correct.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-axelar
- **GitHub**: https://github.com/code-423n4/2022-07-axelar-findings/issues/20
- **Contest**: https://code4rena.com/reports/2022-07-axelar

### Keywords for Search

`vulnerability`

