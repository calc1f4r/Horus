---
# Core Classification
protocol: Solo Margin Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11839
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/solo-margin-protocol-audit-30ac2aaf6b10/
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
  - OpenZeppelin
---

## Vulnerability Title

Malicious AutoTrader contracts may steal funds

### Overview


The Solo contract is a tool that allows users to set any contract as their AutoTrader. However, if a user makes a trade with an attacker using a malicious AutoTrader, the attacker may be able to front-run the trade and steal the full amount of the trade. To prevent this, the dYdX team suggests adding a whitelist of AutoTrader contracts or AutoTrader factories to restrict the possible implementations on-chain. Additionally, the team recommends that users only use contracts that they trust and that an on-chain whitelist of AutoTraders would not prevent malformed or malicious transaction data from producing unintended results.

### Original Finding Content

The Solo contract allows a user to [set any contract as their](https://github.com/dydxprotocol/solo/blob/17df84db351d5438e1b7437572722b4f52c8b2b4/contracts/protocol/impl/OperationImpl.sol#L541) [`AutoTrader`](https://github.com/dydxprotocol/solo/blob/17df84db351d5438e1b7437572722b4f52c8b2b4/contracts/protocol/impl/OperationImpl.sol#L541). If a user makes a trade with an attacker using a malicious [`AutoTrader`](https://github.com/dydxprotocol/solo/blob/17df84db351d5438e1b7437572722b4f52c8b2b4/contracts/protocol/interfaces/IAutoTrader.sol), the attacker may front-run the trade with a transaction that changes the rate returned by the `AutoTrader`‘s `getTradeCost()` effectively allowing the attacker to steal the full amount of the trade.


This can be prevented by only allowing users to interact with approved `AutoTrader` contracts on the front-end. However, it would be best to prevent this attack on-chain rather than relying on off-chain protections.


Consider adding a whitelist of `AutoTrader` contracts or `AutoTrader` factories to restrict the possible implementations on-chain.


*Note: This issue was downgraded from critical severity because the dYdX team is aware of the issue and has plans for off-chain mitigation.*


***Update:*** *Statement from the dYdX team about this issue: “By using the* *`TradeData`* *field,**`AutoTrader`* *contracts can be written so that they do not suffer from any of the security issues mentioned (front running or otherwise). The* *`ExchangeWrapper`* *contracts that we have been using in production for months are secured in this manner.  

As with all smart contracts, users should only use contracts that they trust; it is clearly unsafe to use any arbitrary address for an* *AutoTrader**. Passing in the address of an**`AutoTrader`* *is not less secure than specifying any other data in an Ethereum transaction. An on-chain whitelist of* *`AutoTraders`* *would not prevent malformed or malicious transaction data from producing unintended results.”*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Solo Margin Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/solo-margin-protocol-audit-30ac2aaf6b10/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

