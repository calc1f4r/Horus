---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26068
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/91

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
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - BPZ
  - RED-LOTUS-REACH
  - Koolex
  - yellowBirdy
  - ltyu
---

## Vulnerability Title

[H-34] Cross-chain messaging via `Anycall` will fail

### Overview


This bug report is about a problem with the code in the BranchBridgeAgent.sol and AnycallFlags.sol files in the 0xBugsy (Maia) project. The problem is that the source-fee is not supplied to Anycall when making a cross-chain call, which will cause the call to fail. This will impact many functions that rely on this function, such as callOut(), callOutSigned(), and retryDeposit().

The recommended mitigation steps are to either change the code to use pay on destination, or if pay on source is the intention, to refactor the code to include fees.

The bug report was confirmed and commented on by 0xBugsy (Maia), stating that they recognize the audit's findings on Anycall, but that these will not be rectified due to the upcoming migration of this section to LayerZero.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/ulysses-omnichain/BranchBridgeAgent.sol#L1006-L1011><br><https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/ulysses-omnichain/lib/AnycallFlags.sol#L11>

### Impact

Cross-chain calls will fail since source-fee is not supplied to `Anycall`.

### Proof of Concept

In `_performCall()` of `BranchBridgeAgent.sol`, a cross-chain call is made using `anyCall()` with the `_flag` of [4](https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/ulysses-omnichain/lib/AnycallFlags.sol#L11). According to the [Anycall V7 documentation](https://docs.multichain.org/developer-guide/anycall-v7/how-to-integrate-anycall-v7#request-parameters) and [code](https://github.com/anyswap/multichain-smart-contracts/blob/645d0053d22ed63005b9414b5610879094932304/contracts/anycall/v7/AnycallV7Upgradeable.sol#L205-L207), when using gas `_flag` of 4, the gas fee must be paid on the source chain. This means `anyCall()` must be called and sent gas.

However, this is not the case, and the result of `_performCall` will always revert. This will impact many functions that rely on this function; such as `callOut()`, `callOutSigned()`, `retryDeposit()`, etc.

### Recommended Mitigation Steps

After discussing with the Sponsor, it is expected that the fee be paid on the destination chain, specifically `rootBridgeAgent`. Consider refactoring the code to change the `_flag` to use [pay on destination](https://github.com/anyswap/multichain-smart-contracts/blob/645d0053d22ed63005b9414b5610879094932304/contracts/anycall/v7/interfaces/AnycallFlags.sol#L9).

Alternatively, if pay on source is the intention, consider refactoring the code to include fees; starting with `_performCall`. Additional refactoring will be required.

    function _performCall(bytes memory _calldata, uint256 _fee) internal virtual {
        //Sends message to AnycallProxy
        IAnycallProxy(local`AnyCall`Address).anyCall{value: _fee}(
            rootBridgeAgentAddress, _calldata, rootChainId, AnycallFlags.FLAG_ALLOW_FALLBACK, ""
        );
    }

### Assessed type

Library

**[0xBugsy (Maia) confirmed and commented](https://github.com/code-423n4/2023-05-maia-findings/issues/91#issuecomment-1655680315):**
 > We recognize the audit's findings on Anycall. These will not be rectified due to the upcoming migration of this section to LayerZero.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | BPZ, RED-LOTUS-REACH, Koolex, yellowBirdy, ltyu, xuwinnie |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/91
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

