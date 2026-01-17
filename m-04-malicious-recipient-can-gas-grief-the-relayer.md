---
# Core Classification
protocol: Bob Onramp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34107
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Onramp-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] Malicious recipient can gas grief the relayer

### Overview


Severity: High
Impact: High
Likelihood: Low

Description:
When a user sends BTC on the Bitcoin mainnet, the relayer attempts to execute a swap on the BoB network using an on-ramp contract. The on-ramp contract transfers 1:1 amounts of wrapped BTC and some extra ETH tokens as a gratuity. However, a malicious recipient contract can exploit this by implementing a `receive` function that spends all the transaction gas, causing the function to fail and causing inconvenience to the relayer. This attack can be repeated with small amounts of tokens, potentially leading to a Denial of Service (DoS) of the protocol.

Recommendations:
To prevent this attack, it is recommended to create a pull mechanism instead of sending ETH directly to recipients. This would require recipients to claim the ETH rather than receiving it automatically. This would prevent the malicious recipient contract from causing inconvenience to the relayer.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

When a user sends BTC on the Bitcoin mainnet, the relayer attempts to execute the swap on BoB network with onramp contract

```solidity
    function proveBtcTransfer(
        BitcoinTx.Info memory _txInfo,
        BitcoinTx.Proof memory _txProof,
        address payable _recipient,
        Onramp _onramp
    ) external onlyOwner {
        require(getOnramp[address(_onramp)], "Onramp does not exist");

        bytes32 txHash = relay.validateProof(txProofDifficultyFactor, _txInfo, _txProof);

        uint256 outputValueSat = BitcoinTx.getTxOutputValue(_onramp.scriptPubKeyHash(), _txInfo.outputVector);

        _onramp.executeSwap(txHash, outputValueSat, _recipient);
    }
```

The on-ramp contract transfers 1:1 amounts of wrapped BTC and some extra ETH tokens as gratuity.

```solidity
    function executeSwap(bytes32 _txHash, uint256 _outputValueSat, address payable _recipient) external onlyFactory {
         ---SNIP---

        uint256 amount = calculateAmount(_outputValueSat - feeSat);

        emit ExecuteSwap(_recipient, _outputValueSat, feeSat, amount, gratuity);

        // transfer token
        token.safeTransfer(_recipient, amount);

        // slither-disable-next-line arbitrary-send-eth,low-level-calls
>>      (bool sent,) = _recipient.call{value: gratuity}("");
        require(sent, "Could not transfer ETH");
    }
```

A malicious recipient contract can take advantage of this, by implementing a `receive` function in which it spends all the transaction gas, reverting the function to grief the relayer.
As there is no minimum limit on the BTC amount, except for the `dustThreshold` which can be relatively small, this attack can be repeatedly executed with small amounts of tokens, wasting the relayer's gas. In the worst-case scenario, this could lead to a Denial of Service (DoS) of the protocol.

**Recommendations**

Create a pull mechanism, instead of sending ETH, let recipients claim it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bob Onramp |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Onramp-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

