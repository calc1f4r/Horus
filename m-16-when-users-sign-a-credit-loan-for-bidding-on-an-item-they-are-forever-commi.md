---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15999
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/474

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
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-16] When users sign a credit loan for bidding on an item, they are forever committed to the loan even if the NFT value drops massively

### Overview


A bug has been identified in the ParaSpace marketplace, where a taker can pass a maker's signature and fulfill their bid with the taker's NFT using credit loan. The bug is that the credit structure does not have a deadline, meaning that an attacker can wait and abuse their previous signature to take a larger amount than they would like to pay for the NFT. This leaves the user committed to the loan until the end of time, as there is no revocation mechanism. This bug was discovered through manual audit. 

The impact of this bug is that users signing a credit loan for bidding on an item are forever committed to the loan even if the NFT value drops massively. To mitigate this issue, it is recommended that a deadline timestamp be added to the signed credit structure.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/protocol/libraries/types/DataTypes.sol#L296>

In ParaSpace marketplace, taker may pass maker's signature and fulfil their bid with taker's NFT. The maker can use credit loan to purchase the NFT provided the health factor is positive in the end.

In validateAcceptBidWithCredit, verifyCreditSignature  is called to verify maker signed the credit structure.

    function verifyCreditSignature(
        DataTypes.Credit memory credit,
        address signer,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) private view returns (bool) {
        return
            SignatureChecker.verify(
                hashCredit(credit),
                signer,
                v,
                r,
                s,
                getDomainSeparator()
            );
    }

The issue is that the credit structure does not have a deadline:

    struct Credit {
        address token;
        uint256 amount;
        bytes orderId;
        uint8 v;
        bytes32 r;
        bytes32 s;
    }

As a result, attacker may simply wait and if the price of the NFT goes down abuse their previous signature to take a larger amount than they would like to pay for the NFT. Additionaly, there is no revocation mechanism, so user has completely committed to loan to get the NFT until the end of time.

### Impact

When users sign a credit loan for bidding on an item, they are forever committed to the loan even if the NFT value drops massively.

### Recommended Mitigation Steps

Add a deadline timestamp to the signed credit structure.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/474
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

