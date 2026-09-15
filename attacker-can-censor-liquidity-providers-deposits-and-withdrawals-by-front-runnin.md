---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40759
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 10
finders:
  - qckhp
  - Sujith Somraaj
  - 0xJaeger
  - bronzepickaxe
  - J4X98
---

## Vulnerability Title

Attacker can censor liquidity providers deposits and withdrawals by front-running 

### Overview


This report describes a bug in the Omnipool smart contract, specifically in the depositFor and withdraw functions. The bug allows an attacker to front-run transactions and lock user funds. The impact is high as it can result in loss of user funds, and the likelihood is medium as future users with large amounts of funds may be targeted. The report suggests two possible fixes: restricting deposits to only be made for oneself or removing the lastTransactionBlock checks, although the latter may have unforeseen consequences and requires further study.

### Original Finding Content

## Security Vulnerability in Omnipool's Deposit and Withdraw Functions

## Context
- **Files**: Omnipool.sol#L239, Omnipool.sol#L361

## Description
The `depositFor` and `withdraw` functions in Omnipool require that the address to which funds will be deposited/withdrawn has not executed deposit or withdraw transactions in the current block number. In `depositFor`, this is enforced through a check attached to the finding.

In the `depositFor` function, it is the `_depositFor` address that gets its mapping updated. An attacker can exploit `depositFor` to deposit a small `underlyingToken` amount to the `_depositFor` address. This action will deny the `_depositFor` address from executing any other deposits or withdrawals in the current block. Moreover, as there is no minimum deposit amount, the attack is inexpensive to execute.

### Likelihood and Impact
- **Impact**: High - Loss of user funds.
- **Likelihood**: Medium - Future users will be protocols with large amounts of funds that will be targeted by attackers.

## Proof of Concept
The following code illustrates the structure of `depositFor` and `withdraw`:

```solidity
function depositFor(uint256 _amountIn, address _depositFor, uint256 _minLpReceived) public {
    if (lastTransactionBlock[_depositFor] == block.number) {
        revert CantDepositAndWithdrawSameBlock();
    }
    // Do deposit actions
    lastTransactionBlock[_depositFor] = block.number; // here attacker controls `_depositFor`
}

function withdraw(uint256 _amountOut, uint256 _minUnderlyingReceived) external override {
    if (lastTransactionBlock[msg.sender] == block.number) {
        revert CantDepositAndWithdrawSameBlock();
    }
    // Withdrawal actions
    lastTransactionBlock[msg.sender] = block.number;
}
```

At the early stage of the deposit/withdraw process, the transaction is reverted when the last transaction was executed in the current block. The `_depositFor` is the recipient of the deposit, which is controlled by the attacker.

## Recommendation
Multiple fixes could be implemented:

1. Restrict the protocol so that users can deposit only for themselves.
2. Delete the `lastTransactionBlock` checks. Note that this fix may introduce unexpected issues and should be further studied.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | qckhp, Sujith Somraaj, 0xJaeger, bronzepickaxe, J4X98, kodyvim, kogekar, 0xadrii, zigtur, Victor Okafor |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

