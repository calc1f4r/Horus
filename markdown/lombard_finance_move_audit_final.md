# **Lombard SUI**

Security Assessment


February 18th, 2025 - Prepared by OtterSec


Tuyết Dương [tuyet@osec.io](mailto:tuyet@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-LSI-ADV-00 | Preventing Minting via Front-Running Payload 6


OS-LSI-ADV-01 | Denial of Service via Mint Limit Exhaustion 7


OS-LSI-ADV-02 | Missing Validator Set Integrity Checks 8


**General** **Findings** **9**


OS-LSI-SUG-00 | Prevention of Cross-Chain Replay Attacks 10


**Appendices**


**Vulnerability** **Rating** **Scale** **11**


**Procedure** **12**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 12


**01** **—** **Executive** **Summary**

## Overview


assessment was conducted between January 30th and February 11th, 2025. For more information on


our auditing methodology, refer to Appendix B.

## Key Findings


We produced 4 findings throughout this audit engagement.


In particular, we identified a vulnerability in which the functionality responsible for validating and storing


the payload is susceptible to front-running. This allows an attacker to preemptively mark a valid payload


as utilized, thereby preventing legitimate minting (OS-LSI-ADV-00). Additionally, during the configuration


of the validator set, duplicate validators are not identified, and the correct key lengths are not enforced.


Furthermore, there is no assertion to ensure that the threshold does not exceed the total weight (OS-LSI

ADV-02).


Furthermore, an attacker can repeatedly claim and redeem small coin amounts to exhaust the minting limit


for the epoch, preventing other users from minting new tokens. This effectively creates a denial-of-service


scenario (OS-LSI-ADV-01).


Additionally, we recommended modifying the fee payload structure to include the chain ID to prevent


potential replay attacks (OS-LSI-SUG-00).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 12


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/lombard-finance/sui-](https://github.com/lombard-finance/sui-contracts)


[contracts.](https://github.com/lombard-finance/sui-contracts) This audit was performed against [b3e614c.](https://github.com/lombard-finance/sui-contracts/commit/b3e614c73681c304a515aa3b5e725bf5d7c4c1a7)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


A cross-chain bridge contract that manages deposits and withdrawals


with validation logic. It tracks deposits made on a source chain and

bascule

allows corresponding withdrawals on the destination chain, ensuring


security through validation thresholds.


It manages a decentralized validator set and its governance, enabling


admins to initialize and update validator sets across epochs. It vali
Consortium

dates changes through secure signature checks, payload validation,


and compliance with weight thresholds.


It creates the LBTC coin (a regulated asset-backed 1:1 by BTC) and sets


up a treasury management system with a controlled treasury to manage



lbtc



the coin’s inflow and outflow while ensuring secure coin metadata


through freezing. A multisig address is used to control the treasury,


adding an extra layer of security.



© 2025 Otter Audits LLC. All Rights Reserved. 3 / 12


**03** **—** **Findings**


Overall, we reported 4 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.


© 2025 Otter Audits LLC. All Rights Reserved. 4 / 12


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.



to front-running, allowing an attacker to pre

emptively mark a valid payload as utilized, pre

venting legitimate minting.


to exhaust the minting limit for the epoch, pre

venting other users from minting new tokens.


does not validate duplicate validators, enforce


correct key lengths, or ensure that the threshold


does not exceed the total weight.



OS-LSI-ADV-00


OS-LSI-ADV-01


OS-LSI-ADV-02





© 2025 Otter Audits LLC. All Rights Reserved. 5 / 12


Lombard SUI Audit 04 - Vulnerabilities


**Description**


since it is public, anyone may call it. This creates a potential front-running attack, where a malicious actor


may interfere with the expected execution of a valid transaction. Thus, if a user submits a valid transaction


call.


_>__ _move/consortium/sources/consortium.move_ rust

```
  public fun validate_and_store_payload(
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
  ) {
    // Payload should consist of 164 bytes (160 for message and 4 for the action)
    assert!(payload.length() == 164, EInvalidPayloadLength);
    let hash = hash::sha2_256(payload);
    assert!(!consortium.is_payload_used(hash), EUsedPayload);
    // get the signatures from the proof
    let signatures = payload_decoder::decode_signatures(proof);
    // get the validator set for the current epoch
    let signers = consortium.get_validator_set(consortium.epoch);
    assert!(validate_signatures(signers.pub_keys, signatures, signers.weights,
```

_�→_ `signers.weight_threshold,` `payload,` `hash),` `EInvalidPayload);`
```
    consortium.used_payloads.add(hash, true);
  }

```

**Remediation**


payload tracking is managed within the treasury module.


**Patch**


Resolved in [0fd60cf.](https://github.com/lombard-finance/sui-contracts/commit/0fd60cf39284ff21d4df5bf31bffb871f3429eb3)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 12


Lombard SUI Audit 04 - Vulnerabilities


**Description**


tokens and vice versa. However, an attacker can repeatedly cycle a small token amount between minting


epoch’s minting limit, this exploitation will exhaust the treasury’s capacity within an epoch, preventing


legitimate users from minting new tokens.


**Remediation**


Remove the ability for the user to wrap and unwrap purely inside sui and forces them to go cross-chain,


which should significantly slow down such an attac.


**Patch**


Resolved in [a58183d.](https://github.com/lombard-finance/sui-contracts/commit/a58183df34d0f7f591c4097dd1b3e9be59fe03e7)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 12


Lombard SUI Audit 04 - Vulnerabilities


**Description**


checks, which may allow invalid validator keys. The function does not check for duplicate validator public


keys. There is no validation to ensure that the validator keys are correct and that each validator’s public


key is exactly 65 bytes long.


_>__ _move/consortium/sources/consortium.move_ rust

```
  fun assert_and_configure_validator_set(
    consortium: &mut Consortium,
    action: u32,
    validators: vector<vector<u8>>,
    weights: vector<u256>,
    weight_threshold: u256,
    epoch: u256,
  ) {
    assert!(action == consortium.valset_action, EInvalidAction);
    assert!(validators.length() >= MIN_VALIDATOR_SET_SIZE, EInvalidValidatorSetSize);
    assert!(validators.length() <= MAX_VALIDATOR_SET_SIZE, EInvalidValidatorSetSize);
    assert!(weight_threshold > 0, EInvalidThreshold);
    assert!(validators.length() == weights.length(), EInvalidValidatorsAndWeights);
    [...]
  }

```

**Remediation**


Ensure that each key in the validators list is exactly 65 bytes long.


**Patch**


Resolved in [f825f07.](https://github.com/lombard-finance/sui-contracts/commit/f825f07cd4b36d114f77d7fe661392231ad25f13)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 12


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


OS-LSI-SUG-00

replay attacks.


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 12


Lombard SUI Audit 05 - General Findings


**Prevention** **of** **Cross-Chain** **Replay** **Attacks** OS-LSI-SUG-00


**Description**


fee transactions are only valid on the intended chain, preventing cross-chain replay attacks.


**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 12


**A** **—** **Vulnerability** **Rating** **Scale**


We rated our findings according to the following scale. Vulnerabilities have immediate security implications.


Informational findings may be found in the General Findings.


Examples:


         - Misconfigured authority or access control validation.


         - Improperly designed economic incentives leading to loss of funds.


Vulnerabilities that may result in a loss of user funds but are potentially difficult to exploit.


Examples:


         - Loss of funds requiring specific victim interactions.


         - Exploitation involving high capital requirement with respect to payout.


Examples:


         - Computational limit exhaustion through malicious input.


         - Forced exceptions in the normal user flow.


or undue risk.


Examples:


         - Oracle manipulation with large capital requirements and multiple transactions.


Examples:


         - Explicit assertion of critical internal invariants.


         - Improved input validation.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 12


**B** **—** **Procedure**


As part of our standard auditing procedure, we split our analysis into two main sections: design and


implementation.


When auditing the design of a program, we aim to ensure that the overall economic architecture is sound


in the context of an on-chain program. In other words, there is no way to steal funds or deny service,


ignoring any chain-specific quirks. This usually requires a deep understanding of the program’s internal


interactions, potential game theory implications, and general on-chain execution primitives.


One example of a design vulnerability would be an on-chain oracle that could be manipulated by flash


loans or large deposits. Such a design would generally be unsound regardless of which chain the oracle


is deployed on.


On the other hand, auditing the program’s implementation requires a deep understanding of the chain’s


execution model. While this varies from chain to chain, some common implementation vulnerabilities


include reentrancy, account ownership issues, arithmetic overflows, and rounding bugs.


As a general rule of thumb, implementation vulnerabilities tend to be more “checklist” style. In contrast,


design vulnerabilities require a strong understanding of the underlying system and the various interactions:


both with the user and cross-program.


As we approach any new target, we strive to comprehensively understand the program first. In our audits,


we always approach targets with a team of auditors. This allows us to share thoughts and collaborate,


picking up on details that others may have missed.


While sometimes the line between design and implementation can be blurry, we hope this gives some


insight into our auditing procedure and thought process.


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 12


