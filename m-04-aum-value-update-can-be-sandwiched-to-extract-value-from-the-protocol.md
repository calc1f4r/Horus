---
# Core Classification
protocol: Fyde
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31702
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] AUM value update can be sandwiched to extract value from the protocol

### Overview


This bug report discusses a high severity issue in a protocol where an attacker can manipulate the AUM value to perform a sandwich attack and extract value from the protocol. The attacker can do this by monitoring the off-chain bot's AUM update transaction and then depositing and withdrawing tokens to receive more tokens than they initially had. To prevent this, the report recommends implementing measures such as not allowing withdrawals and deposits in the same block and adding a delay for withdrawals or deposits.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

Protocol requires the off-chain bot to update AUM value so it can compute the share amount in deposited/withdrawal function and the attacker can use this to his advantage and perform the sandwich attack to extract value from the protocol. This is the POC:

1. Suppose the price of T1 token is 1 and protocol's `AUM` is $98K and `totalShare` is $98K.
2. Attacker monitoring mempool saw the off-chain bot AUM update transaction to set AUM as $102K.
3. Now attacker would perform this sandwich attack:
4. Before AUM update attacker would deposit 2K T1 tokens and receive 2K shares and `totalShare` and `AUM` will be $100K.
5. Then AUM update tx will be executed and AUM would be set as $102K.
6. Now attacker would withdraw 2.04K T1 tokens and code would calculate shares as `shares = token * price * totalShare / AUM = 2.04 * 1 * 100K / 102K = 2K` and transfer 2.04K T1 token while burning user's 2K shares.
7. At the end user received 0.04K tokens more.

**Recommendations**

Don't allow withdraw and deposit in the same block for each user to make the attack harder.
Use the same AUM value for the whole block.
Add delay for withdrawal or deposit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

