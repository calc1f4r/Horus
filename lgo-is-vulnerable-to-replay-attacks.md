---
# Core Classification
protocol: Level Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60874
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
source_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
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
finders_count: 4
finders:
  - Jeffrey Kam
  - Mustafa Hasan
  - Rabib Islam
  - Guillermo Escobero
---

## Vulnerability Title

LGO is Vulnerable to Replay Attacks

### Overview


This report discusses a bug found in the `LevelGovernance.sol` file. The `DOMAIN_SEPARATOR` value is not initialized, which means that valid signatures can be reused for other applications that follow the same signature procedure. This could potentially lead to an exploit scenario where someone could replay a signature and gain access to a user's tokens. The recommendation is to initialize the `DOMAIN_SEPARATOR` in the initializer or upgrade the contract to enable setting the initializer. The report also provides a possible solution for initializing the `DOMAIN_SEPARATOR` and recommends referring to EIP-712 for more information.

### Original Finding Content

**Update**
Fixed. However, the team still has to upgrade the contract and set the domain initializer. The client's response: "Fixed via level-fi/level-core-contracts#58ad470a1921f0f54d4a923aef03eec69f8cbfa0"

**File(s) affected:**`LevelGovernance.sol`

**Description:** The `DOMAIN_SEPARATOR` value used in multiple functions to render signatures only usable for this specific protocol is never initialized. This effectively means that valid signatures can be reused with other applications that follow the same signature procedure.

**Exploit Scenario:**

1.   Alice signs a `permit` message to Bob in protocol X. Protocol X also implements a nonce system, but the `DOMAIN_SEPARATOR` is also zero. This is the first signed message of Alice in Protocol X, so the nonce will be zero. `PERMIT_TYPEHASH` in protocol X is equal to Level's (common ERC-20 function).
2.   Bob notices that Alice is a `LGO` holder.
3.   Bob replays the signature calling `LevelGovernance.permit()`.

**Recommendation:** Initialize `DOMAIN_SEPARATOR` in the initializer. If the contract is already deployed, consider upgrading the contract in order to enable setting the initializer. A possible domain separator initialization may appear as follows:

```
uint256 chainId;

assembly {
    chainId := chainid()
}

DOMAIN_SEPARATOR = keccak256(abi.encode(
    EIP712_DOMAIN,
    keccak256(bytes(name)),
    keccak256(EIP712_REVISION),
    chainId,
    address(this)
));
```

See [EIP-712](https://eips.ethereum.org/EIPS/eip-712#definition-of-domainseparator) for further information and recommendations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Level Finance |
| Report Date | N/A |
| Finders | Jeffrey Kam, Mustafa Hasan, Rabib Islam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html

### Keywords for Search

`vulnerability`

