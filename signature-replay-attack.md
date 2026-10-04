---
# Core Classification
protocol: Primex Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59034
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
source_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
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
finders_count: 4
finders:
  - Jennifer Wu
  - Andy Lin
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Signature Replay Attack

### Overview


This bug report discusses an issue with three contracts in the Primex finance system. These contracts are vulnerable to cross-chain signature replay, which means that signed messages can be used indefinitely on different networks. This could potentially lead to security risks and fake referral connections. The report recommends implementing the EIP712 standard or adding a chain ID and expiration date to the signed messages to mitigate this risk. It also suggests incorporating an expiration timestamp to limit the duration of signature validity. The severity of this issue has been escalated to medium and it is important to address it proactively to ensure the long-term security and stability of the system.

### Original Finding Content

**Update**
The team acknowledged the issue with a detailed statement as follow:

> This issue touches several contracts, so comments are also separated: 1) NFT: We do not want to restrict the ability to mint NFTs for users who have received a signature from NFT_MINTER, so the absence of an expiration date is acceptable. We also have additional security measures in place that allow us to pause reward distribution and block incorrect NFTs according to protocol management rules.
> 
> 
> 2) Referral whitelist: We have decided to remove the requirement for whitelisting to become a referrer. Now, anyone can generate a signature that serves as a referral link and invite other users. The requirement for referrers to be whitelisted will be eliminated from the contracts.
> 
> 
> 3) Referral program: We have decided to independently launch the referral program on each network where Primex will be deployed. Additionally, we do not want to require the referrer and referee to be users of the same network. Therefore, referrers will generate universal signatures that can be used by referees on any EVM network. As a result, we do not need to add a chain Id. Referral links will be valid indefinitely, ensuring a positive experience for referrers and referees without any risks for misbehaving referees.
> 
> 
> The smart contracts for the referral program will solely serve the purpose of storing connections between users. The reward distribution for referrers will be calculated off-chain, taking into consideration referral connections across different networks. In cases of conflicts, the connection created earlier will be considered correct. The distribution algorithm will also be Sybil-resistant to protect the protocol from bots that generate fake referral connections. More information can be found in the answer to [PRI-54](https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html#findings-qs54).

**File(s) affected:**`WhiteBlackListReferral.sol`, `PMXBonusNFT.sol`, `ReferralProgram.sol`

**Description:** The following contracts are susceptible to cross-chain signature replay due to a lack of chain id and expiration mechanisms in their signed messages:

1.   The PMX bonus NFT allows for the signing of minting parameters, dictating the type of bonus that can be activated by its owner. While the signature hashes the `MintParameters` which include the chain ID, it lacks an expiration date. This means the parameters remain valid indefinitely and new NFTs can be always minted with the signed parameters. Given that only those with the `NFT_MINTER` role can access the mint function, this issue serves primarily as an informational note.

2.   The referral whitelist enables users to enroll as referrers in the referral program. The signed message contains the contract name, function, and referrer. However, if the whitelist contract is deployed across multiple chains using the same signer, the signature remains valid indefinitely on all chains. This is due to the omission of both chain ID and an expiration date in the signature.

3.   The referral system permits signing referral messages without incorporating expiration dates or chain IDs. This design allows the message to be used across any EVM-compatible chain, and without a set expiration, the referral message remains valid indefinitely. It is crucial to inform referrers of these cross-chain signature replay risks when generating signed messages.

For the replay attack on the referral contracts to be successful, certain additional conditions must be met. For instance, the signer must be whitelisted or be the admin in multiple chains. Additionally, based on our discussion with the PrimeX team, even though the protocol aims to be deployed on multiple chains, they plan to run the referral program on only one chain. Therefore, the risk is relatively low in this scenario.

Nonetheless, we strongly urge addressing this issue despite the low risk, as the situation can change or the assumptions can be invalidated depending on the operation. It is crucial to proactively mitigate any potential vulnerabilities to ensure the long-term security and stability of the system. As a result, we escalated the severity to medium for this issue.

**Recommendation:** Consider following the [EIP712 standard](https://eips.ethereum.org/EIPS/eip-712), which includes the chain ID and the contract address as part of the signature, to mitigate the risk of a replay attack. Alternatively, at the very least, incorporate the chain ID and the contract address into the signed messages if not adhering to the standard.

Additionally, we suggest incorporating an expiration timestamp into all signatures to limit the duration of signature validity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Primex Finance |
| Report Date | N/A |
| Finders | Jennifer Wu, Andy Lin, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html

### Keywords for Search

`vulnerability`

