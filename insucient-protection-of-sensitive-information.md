---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17693
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
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
  - Troy Sargent
  - Anish Naik
  - Nat Chin
---

## Vulnerability Title

Insu�cient protection of sensitive information

### Overview


This bug report is about the potential compromise of sensitive information such as mnemonic seed phrases and API keys stored in process environments and environment files. These environment files are stored in the CrosslayerPortal/env and bribe-protocol/hardhat.config.ts files, and if the repository is made public, the Git commit history will retain the API keys in plaintext. This could allow an attacker to gain access to the owner's mnemonic seed phrase and steal all funds.

Short-term recommendations include using a hardware security module to ensure the keys cannot be extracted, and avoiding hard-coded secrets and committing environment files to version control systems. Long-term recommendations include moving key material to a dedicated secret management system with trusted computing abilities, such as Google Cloud Key Management System and Hashicorp Vault (with hardware security module backing), and determining the business risk that would result from a lost or stolen key and developing disaster recovery and business continuity policies to be implemented in such a case.

### Original Finding Content

## Diﬃculty: Undetermined

## Type: Data Validation

## Target: 
- CrosslayerPortal/env
- bribe-protocol/hardhat.config.ts

## Description
Sensitive information such as a mnemonic seed phrase and API keys is stored in process environments and environment files. This method of storage could make it easier for an attacker to compromise the information; compromise of the seed phrase, for example, could enable an attacker to gain owner privileges and steal funds from the protocol.

The following portion of the `bribe-protocol/hardhat.config.ts` file uses a mnemonic seed phrase from the process environment:

```javascript
mainnet: {
  accounts: {
    mnemonic: process.env.MNEMONIC || "",
  },
  url: "https://eth-mainnet.alchemyapi.io/v2/XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
},
```

_Figure 30.1: Use of a mnemonic seed phrase from the process environment in the bribe-protocol/hardhat.config.ts file_

The following portion of the `CrosslayerPortal/env/mainnet.env` file exposes Etherscan and Alchemy API keys:

```env
NETWORK_NAME=mainnet
CHAIN_ID=1
## API
BLOCK_EXPLORER_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALCHEMY_API=https://eth-mainnet.alchemyapi.io/v2/XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

_Figure 30.2: Exposed API keys in the CrosslayerPortal/env/mainnet.env file_

If this repository is ever made public, the Git commit history will retain these API keys in plaintext. Access to the Alchemy API key, for example, would allow an attacker to launch a DoS attack on the application’s front end.

## Exploit Scenario
Alice has the owner’s mnemonic seed phrase stored in her process environment. Eve, an attacker, gains access to Alice’s device and extracts the seed phrase from it. Eve uses the owner key to steal all funds.

## Recommendations
**Short term**, use a hardware security module to ensure that none of the keys can be extracted. Additionally, avoid using hard-coded secrets and committing environment files to version control systems.

**Long term**, take the following steps:
- Move key material from environment variables to a dedicated secret management system with trusted computing abilities. The best options for such a system are the Google Cloud Key Management System and Hashicorp Vault (with hardware security module backing).
- Determine the business risk that would result from a lost or stolen key and develop disaster recovery and business continuity policies to be implemented in such a case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Troy Sargent, Anish Naik, Nat Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ12022.pdf

### Keywords for Search

`vulnerability`

