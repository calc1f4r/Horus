---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32130
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-canto
source_link: https://code4rena.com/reports/2024-03-canto
github_link: https://github.com/code-423n4/2024-03-canto-findings/issues/5

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - d3e4
  - oakcobalt
  - 0xTheC0der
---

## Vulnerability Title

[H-02] Dual transaction nature of composed message transfer allows anyone to steal user funds

### Overview


The bug report discusses an issue with sending composed messages using LayerZero V2. The process involves two separate transactions on the destination chain, which can be exploited by an attacker to steal user funds. This is due to the permissionless nature of the execution step, which allows anyone to invoke it. The report suggests restricting the execution step to trusted/whitelisted executors or implementing a design change to eliminate the need for composed messages. The bug has been confirmed and a pull request has been submitted to fix it.

### Original Finding Content



Sending OFTs with a composed message via LayerZero V2 involves 2 transactions on the destination chain (Canto) according to the [documentation](https://docs.layerzero.network/v2/developers/evm/oft/quickstart# optional-_composedmsg) (see also [README](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/README.md?plain=1# L199)):

1. Receiving: The LayerZero endpoint receives the message and processes the OFT transfer to the `ASDRouter` contract.
2. Executing: Since the message is composed, it’s *permissionlessly* processed by an executor who invokes the [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) method of the `ASDRouter` contract.

The above steps are processed in separate transactions (not atomic) and step 2 requires the OFTs [to be already transferred](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/README.md?plain=1# L89) to the `ASDRouter` contract.

Furthermore, due to the permissionless nature of the execution step, the [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) method does not enforce any constraints on the `msg.sender`; therefore, allows anyone to invoke it.

**Attack path:**

An adversary can monitor the `ASDRouter` contract for [whitelisted](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L79) incoming USDC-like OFTs and immediately use those on their own (redeem `asD`) by crafting & invoking a call to [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) before an executor does. As a consequence, user funds are directly stolen.

Similarly, if [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) fails for any reason, an adversary can re-try before the user to use the OFTs.

### Proof of Concept

The dual transaction nature of the current composed message process is confirmed by the LayerZero [documentation](https://docs.layerzero.network/v2/developers/evm/oft/quickstart# optional-_composedmsg):

> If the message is composed, the contract retrieves and re-encodes the additional composed message information, then delivers the message to the endpoint, which will execute the additional logic as a separate transaction.

Moreover, crafting a successful call to [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) once OFTs are deposited is demonstrated by the existing test case [“lzCompose: successful deposit and send on canto”](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/test/ASDRouter.js# L276-L297).

### Recommended Mitigation Steps

Immediate, but not a satisfying fix: Restrict the [lzCompose(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdRouter.sol# L52-L111) method to trusted/whitelisted executors.

Alternative: Design change by directly implementing [`_lzReceive`(…)](https://docs.layerzero.network/v2/developers/evm/oapp/overview# implementing-_lzreceive) (building an `OApp`) such that a composed message is not needed anymore.

### Assessed type

Invalid Validation

**[3docSec (judge) commented](https://github.com/code-423n4/2024-03-canto-findings/issues/5# issuecomment-2036426301):**

> Looks legitimate: `lzCompose` is permissionless and can be front-run because [LayerZero calls it in a separate transaction after funds are delivered](https://github.com/LayerZero-Labs/LayerZero-v2/blob/1fde89479fdc68b1a54cda7f19efa84483fcacc4/oapp/contracts/oft/OFTCore.sol# L238C1-L253C10).

**[dsudit01 (Canto) confirmed and commented](https://github.com/code-423n4/2024-03-canto-findings/issues/5# issuecomment-2040524459):**

> PR [here](https://github.com/Plex-Engineer/ASD-V2/pull/4).

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | d3e4, oakcobalt, 0xTheC0der |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-canto
- **GitHub**: https://github.com/code-423n4/2024-03-canto-findings/issues/5
- **Contest**: https://code4rena.com/reports/2024-03-canto

### Keywords for Search

`vulnerability`

