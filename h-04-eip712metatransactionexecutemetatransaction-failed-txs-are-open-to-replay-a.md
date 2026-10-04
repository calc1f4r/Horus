---
# Core Classification
protocol: Rolla
chain: everychain
category: uncategorized
vulnerability_type: replay_attack

# Attack Vector Details
attack_type: replay_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1685
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-rolla-contest
source_link: https://code4rena.com/reports/2022-03-rolla
github_link: https://github.com/code-423n4/2022-03-rolla-findings/issues/45

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - replay_attack
  - nonce

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-04] EIP712MetaTransaction.executeMetaTransaction() failed txs are open to replay attacks

### Overview


This bug report is about an issue found in the implementation of the EIP712MetaTransaction.sol contract. The issue is that when a transaction fails due to certain conditions, the nonce of the transaction does not get incremented. This allows anyone to replay the same transaction with the same signature, which can lead to unexpected fund loss.

To demonstrate the issue, an example is given. Alice has 10,000 USDC in her wallet. She submits a MetaTransaction to operate and _mintOptionsPosition with 10,000 USDC. Before the MetaTransaction is executed, Alice sends 1,000 USDC to Bob. The MetaTransaction submitted by Alice fails, and a few days later Bob sends 1,000 USDC to Alice. The attacker can then replay the MetaTransaction that failed to execute and succeed, leading to Alice's 10,000 USDC being spent unexpectedly and potentially causing fund loss.

The recommendation given to resolve this issue is to ensure that failed transactions still increase the nonce. Additionally, it is suggested to add a check to require sufficient gas to be paid to prevent "insufficient gas griefing attack".

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-03-rolla/blob/efe4a3c1af8d77c5dfb5ba110c3507e67a061bdd/quant-protocol/contracts/utils/EIP712MetaTransaction.sol#L86


## Vulnerability details

Any transactions that fail based on some conditions that may change in the future are not safe to be executed again later (e.g. transactions that are based on others actions, or time-dependent etc).

In the current implementation, once the low-level call is failed, the whole tx will be reverted and so that `_nonces[metaAction.from]` will remain unchanged.

As a result, the same tx can be replayed by anyone, using the same signature.

https://github.com/code-423n4/2022-03-rolla/blob/efe4a3c1af8d77c5dfb5ba110c3507e67a061bdd/quant-protocol/contracts/utils/EIP712MetaTransaction.sol#L86

```solidity
    function executeMetaTransaction(
        MetaAction memory metaAction,
        bytes32 r,
        bytes32 s,
        uint8 v
    ) external payable returns (bytes memory) {
        require(
            _verify(metaAction.from, metaAction, r, s, v),
            "signer and signature don't match"
        );

        uint256 currentNonce = _nonces[metaAction.from];

        // intentionally allow this to overflow to save gas,
        // and it's impossible for someone to do 2 ^ 256 - 1 meta txs
        unchecked {
            _nonces[metaAction.from] = currentNonce + 1;
        }

        // Append the metaAction.from at the end so that it can be extracted later
        // from the calling context (see _msgSender() below)
        (bool success, bytes memory returnData) = address(this).call(
            abi.encodePacked(
                abi.encodeWithSelector(
                    IController(address(this)).operate.selector,
                    metaAction.actions
                ),
                metaAction.from
            )
        );

        require(success, "unsuccessful function call");
        emit MetaTransactionExecuted(
            metaAction.from,
            payable(msg.sender),
            currentNonce
        );
        return returnData;
    }
```

See also the implementation of OpenZeppelin's `MinimalForwarder`:

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.5.0/contracts/metatx/MinimalForwarder.sol#L42-L66

### PoC

Given:

- The collateral is USDC;
- Alice got `10,000 USDC` in the wallet.

1. Alice submitted a MetaTransaction to `operate()` and `_mintOptionsPosition()` with `10,000 USDC`;
2. Before the MetaTransaction get executed, Alice sent `1,000 USDC` to Bob;
3. The MetaTransaction submited by Alice in step 1 get executed but failed;
4. A few days later, Bob sent `1,000 USDC` to Alice;
5. The attacker can replay the MetaTransaction failed to execute at step 3 and succeed.

Alice's `10,000 USDC` is now been spent unexpectedly against her will and can potentially cause fund loss depends on the market situation.

### Recommendation

Failed txs should still increase the nonce.

While implementating the change above, consider adding one more check to require sufficient gas to be paid, to prevent "insufficient gas griefing attack" as described in [this article](https://ipfs.io/ipfs/QmbbYTGTeot9ic4hVrsvnvVuHw4b5P7F5SeMSNX9TYPGjY/blog/ethereum-gas-dangers/).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Rolla |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-rolla
- **GitHub**: https://github.com/code-423n4/2022-03-rolla-findings/issues/45
- **Contest**: https://code4rena.com/contests/2022-03-rolla-contest

### Keywords for Search

`Replay Attack, Nonce`

