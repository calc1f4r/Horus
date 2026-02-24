---
# Core Classification
protocol: Hyperstable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55696
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
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
  - @IAm0x52
---

## Vulnerability Title

[M-02] Airdrop supply methodology has been changed leading to excess token emissions

### Overview


This bug report discusses a difference in the way tokens are distributed in two smart contracts, `MerkleClaim` and `PegAirdrop`. The `MerkleClaim` contract uses on-demand minting, while the `PegAirdrop` contract distributes tokens from a pre-existing supply. This difference can lead to excess token emissions in the `epochEmission` function of the `EmissionScheduler` contract. The recommendation is to remove the balance of `PegAirdrop` from the emission calculation or to use on-demand minting in both contracts. The bug has been fixed in the latest version of the `EmissionScheduler` contract.

### Original Finding Content

**Details**

[MerkleClaim.sol#L48-L69](https://github.com/velodrome-finance/v1/blob/de6b2a19b5174013112ad41f07cf98352bfe1f24/contracts/redeem/MerkleClaim.sol#L48-L69)

        function claim(
            address to,
            uint256 amount,
            bytes32[] calldata proof
        ) external {
            // Throw if address has already claimed tokens
            require(!hasClaimed[to], "ALREADY_CLAIMED");

            // Verify merkle proof, or revert if not in tree
            bytes32 leaf = keccak256(abi.encodePacked(to, amount));
            bool isValidLeaf = MerkleProof.verify(proof, merkleRoot, leaf);
            require(isValidLeaf, "NOT_IN_MERKLE");

            // Set address to claimed
            hasClaimed[to] = true;

            // Claim tokens for address
    @>      require(VELO.claim(to, amount), "CLAIM_FAILED");

            // Emit claim event
            emit Claim(to, amount);
        }

Above is the original `VELO` `MerkleClaim` code. Observe that when claiming, `VELO` is minted on demand. This is contrasted with `PegAirdrop` (`MerkleClaim` fork) which holds all the tokens and simply distributes them as users claim.

[EmissionScheduler.sol#L63-L80](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L63-L80)

        function epochEmission(uint256 _pegSupply, uint256 _veSupply) external returns (uint256, uint256, uint256) {
            uint256 currentEpoch = _currentEpoch();

            if (currentEpoch == lastEpoch) {
                return (0, 0, 0);
            }

            lastEpoch = currentEpoch;

    @>      uint256 toEmit = (_pegSupply - _veSupply).mulDiv(2, EMISSION_PRECISION);

            lastEpochEmission = toEmit;

            uint256 rebase = _calculateRebase(toEmit, _pegSupply, _veSupply);
            uint256 teamEmission = _calculateTeamEmission(toEmit, rebase);

            return (toEmit, rebase, teamEmission);
        }

This difference is quite important as `epochEmission` is based on the float percentage of `supply`. As a result these tokens which are undistributed will be incorrectly counted against the floating token `supply`. This will lead to excess token emissions until the claim period is over governance is able to recover them.

**Lines of Code**

[EmissionScheduler.sol#L72](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L72)

**Recommendation**

Consider removing the balance of `PegAirdrop` from the emission calculation or using an on-demand minting strategy similar to `VELO`.

**Remediation**

Fixed in [85be083](https://github.com/hyperstable/contracts/commit/85be083579af51f7c04b39233d8daab96bb40ff1). Distribution has been changed to on-demand minting.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Hyperstable |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

