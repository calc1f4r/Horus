---
# Core Classification
protocol: Unikura
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60429
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/unikura/8ffefcd3-11eb-41ce-9ae8-f550d7df5c99/index.html
source_link: https://certificate.quantstamp.com/full/unikura/8ffefcd3-11eb-41ce-9ae8-f550d7df5c99/index.html
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
  - Zeeshan Meghji
  - Danny Aksenov
  - Gelei Deng
---

## Vulnerability Title

Privileged Roles and Ownership

### Overview


The client has acknowledged an issue with multiple contracts in the project that have privileged roles with special permissions. These contracts include `UnikuraMembership.sol`, `UnikuraMothership.sol`, and `UnikuraPhygitalCollection.sol`. The privileged roles in these contracts have the ability to mint membership NFTs, set token metadata and sales addresses, and burn tokens. The report recommends documenting the risks and potential impact of these privileged roles and implementing additional security measures such as multi-sig or timelock features to mitigate the risk of exploitation. 

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We're going to provide this document when launching. https://velvett.gitbook.io/unikura/about-unikura/what-is-unikura

**File(s) affected:**`UnikuraPhygitalCollection.sol`, `UnikuraMothership.sol`, `UnikuraMembership.sol`

**Description:** Multiple contracts under audit feature privileged roles with special permission. It is also important for project users to be aware of the privileged roles and their permissions so that they are aware of all potential risks. All of the below contracts feature some privileged roles:

1.   `UnikuraMembership`

    1.   `owner`

        1.   Mint a gold or silver membership NFT to any address: `mint()`.
        2.   Set the URI for the token metadata: `setURI()`.
        3.   Set the sales address for the token: `setSalesAddress()`.
        4.   Set the address which can burn tokens `setBurnAddress()`.

    2.   `burnAddress`: Can burn any tokens from any address: `burn()`.

    3.   `salesAddress`: May hold more than one membership token at a time.

2.   `UnikuraMothership`: `owner`:

    1.   Set the fee percentage: `setFeePercentage()`.
    2.   Set the fee recipient address: `setVelvettFeeRecipient()`.
    3.   Set the address of the membership contract: `setUnikuraMembershipContract()`.

3.   `UnikuraPhygitalCollection`: `owner`:

    1.   Set the URI for the token metadata: `setBaseURI()`.
    2.   Set the address of the mothership contract: `setUnikuraMothershipContract()`.
    3.   Set the sales address: `setSalesAddress()`.
    4.   Set the mint price per token `setMintPrice()`.

**Recommendation:** Consider documenting the risk and impact a compromised privileged role can cause on the protocol and inform the users in detail. As the privileged roles can be the single point of failure of the protocol, consider using a multi-sig or a contract with a timelock feature to mitigate the risk of being compromised or exploited.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Unikura |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Danny Aksenov, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/unikura/8ffefcd3-11eb-41ce-9ae8-f550d7df5c99/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/unikura/8ffefcd3-11eb-41ce-9ae8-f550d7df5c99/index.html

### Keywords for Search

`vulnerability`

