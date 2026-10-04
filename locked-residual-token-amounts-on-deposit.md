---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56810
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy%20(2)/README.md#1-locked-residual-token-amounts-on-deposit
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
  - MixBytes
---

## Vulnerability Title

Locked Residual Token Amounts on Deposit

### Overview


The bug report describes an issue in the `P2pYieldProxy._deposit` function where the proxy does not properly handle the leftover balance after deducting fees. This results in user funds being unintentionally locked and inaccessible. The report recommends forwarding the residual amount to the treasury to prevent this issue. The client has already fixed the bug in their code.

### Original Finding Content

##### Description
In `P2pYieldProxy._deposit` (ERC-20 branch) the proxy pulls `amount` tokens from the client but forwards only `amountToDepositAfterFee = amount * s_clientBasisPointsOfDeposit / 10 000` to the underlying protocol. The difference (`amount – amountToDepositAfterFee`) remains in the proxy with no subsequent path for withdrawal or accounting. As deposits and withdrawals track only the forwarded value, this leftover balance becomes inaccessible, resulting in user funds being unintentionally locked.

While the balance is not permanently lost, as governance could whitelist an auxiliary deposit call in `AllowedCalldataChecker` and then push the leftover through `callAnyFunction` to a connected yield protocol, doing so requires out-of-band intervention, breaks the current fee-accounting model, and creates a window where funds are effectively frozen and untracked. These factors justify **High** severity.
<br/>
##### Recommendation
We recommend forwarding the residual amount to the treasury, ensuring no token balance remains orphaned inside the proxy.

> **Client's Commentary:**
> Fixed in https://github.com/p2p-org/p2p-lending-proxy/commit/b7b2a4ff5b321afa7d9edaddf62953411eab8ff0

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Lending%20Proxy%20(2)/README.md#1-locked-residual-token-amounts-on-deposit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

