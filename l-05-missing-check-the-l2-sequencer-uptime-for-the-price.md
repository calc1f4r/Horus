---
# Core Classification
protocol: SXT_2025-03-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63324
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-05] Missing check the L2 sequencer uptime for the price

### Overview

See description below for full details.

### Original Finding Content


In function `_validatePriceFeed`, we will fetch the price's feed from chainlink's feed. When we try to fetch price from Layer2, it's suggested that we should check the sequencer's uptime and pass the grace period and then fetch the price.(https://docs.chain.link/data-feeds/l2-sequencer-feeds)

According to the sponsor's input, contracts may be deployed on Base chain. So if the contract is deployed on Base chain, we need to consider checking the sequencer's uptime.

```solidity
    function _validateSxtFulfillUnstake(
        address staker,
        uint248 amount,
        uint64 sxtBlockNumber,
        bytes32[] calldata proof,
        bytes32[] calldata r,
        bytes32[] calldata s,
        uint8[] calldata v
    ) internal view returns (bool isValid) {
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encodePacked(uint256(uint160(staker)), amount))));
        bytes32 rootHash = MerkleProof.processProof(proof, leaf);
        bytes32 messageHash =
            keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n36", rootHash, sxtBlockNumber, block.chainid));

        isValid =
            ISubstrateSignatureValidator(SUBSTRATE_SIGNATURE_VALIDATOR_ADDRESS).validateMessage(messageHash, r, s, v);
    }

```

Add sequencer's uptime check if the deployed chain is Base chain.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | SXT_2025-03-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SXT-security-review_2025-03-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

