---
# Core Classification
protocol: WinWin Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51563
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/winwin/winwin-protocol-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/winwin/winwin-protocol-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

Centralization risk: Random numbers that determine the winner are selected off-chain

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the current implementation of the protocol the winners are determined based of random numbers generated off-chain which then are added to the `RandomNumber` contract through the `setRandomNumber()` function, only callable by an admin:

![RandomNumber.setRandomNumber() function](https://halbornmainframe.com/proxy/audits/images/6655d10c76dc63e34813ad17)

Using off-chain random number generation for determining the winners introduces several significant issues:

1. **Centralization Risk:**

   * The reliance on an off-chain source for randomness and the need for an admin to set the random number means that the entire system is dependent on a central authority. This central point of control can be exploited or corrupted.
2. **Lack of Transparency:**

   * Participants in the raffle have no way to verify the fairness of the random number. The process is opaque, and users must trust the admin to act honestly, which undermines the trustless nature of blockchain technology.
3. **Potential for Manipulation:**

   * The admin, or anyone with control over the off-chain random number generator, can manipulate the outcome of the raffle by choosing favorable random numbers. This opens the door to fraud and reduces the integrity of the protocol.
4. **Single Point of Failure:**

   * If the off-chain random number generator or the admin’s ability to set the random number is compromised, the entire raffle system can be disrupted.

##### **Alternatives for Secure and Trustless Random Number Generation**

1. **Chainlink VRF (Verifiable Random Function):**

   * **Description:** Chainlink VRF provides a provably fair and verifiable source of randomness. It is a decentralized oracle service that generates random numbers that can be verified by anyone.
   * **Implementation:**

     ```
     import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

     contract Raffle is VRFConsumerBase {
         bytes32 internal keyHash;
         uint256 internal fee;
         uint256 public randomResult;

         constructor() 
             VRFConsumerBase(
                 0x514910771AF9Ca656af840dff83E8264EcF986CA, // VRF Coordinator
                 0x514910771AF9Ca656af840dff83E8264EcF986CA  // LINK Token
             ) {
             keyHash = 0xAA77729D3466CA35AE8D28FA0D0B6AEE3B7D2B13;
             fee = 0.1 * 10 ** 18; // 0.1 LINK
         }

         function getRandomNumber() public returns (bytes32 requestId) {
             require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK");
             return requestRandomness(keyHash, fee);
         }

         function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
             randomResult = randomness;
         }
     }
     ```
   * **Pros:** Decentralized, secure, and verifiable.
   * **Cons:** Requires LINK tokens and depends on the Chainlink network.
2. **Ethereum Beacon Chain Randomness (RANDAO):**

   * **Description:** The Ethereum 2.0 Beacon Chain includes a randomness beacon that can be used for generating random numbers. It leverages the RANDAO protocol for secure and decentralized randomness.
   * **Implementation:** This method is more suitable for contracts deployed on Ethereum 2.0 and would require interfacing with the Beacon Chain’s randomness features.
3. **Commit-Reveal Scheme:**

   * **Description:** This scheme involves participants committing to a random number without revealing it, then revealing the number in a later transaction. The final random number is derived from these committed numbers.
   * **Implementation:**

     ```
     contract Raffle {
         struct Commitment {
             bytes32 hash;
             bool revealed;
             uint256 number;
         }
         mapping(address => Commitment) public commitments;

         function commit(bytes32 hash) public {
             commitments[msg.sender] = Commitment({hash: hash, revealed: false, number: 0});
         }

         function reveal(uint256 number) public {
             Commitment storage commitment = commitments[msg.sender];
             require(commitment.hash == keccak256(abi.encodePacked(number)), "Invalid reveal");
             require(!commitment.revealed, "Already revealed");
             commitment.revealed = true;
             commitment.number = number;
         }

         function determineWinner() public view returns (address winner) {
             // Logic to determine the winner based on revealed numbers
         }
     }
     ```
   * **Pros:** Decentralized and trustless.
   * **Cons:** More complex and requires participant involvement in both commit and reveal phases.
4. **Using Blockhash:**

   * **Description:** Use the hash of a future block as a source of randomness.
   * **Example implementation:**

     ```
     // This code has not been professionally audited, therefore I cannot make any promises about
     // safety or correctness. Use at own risk.
     contract Randomness {

         bytes32 sealedSeed;
         bool seedSet = false;
         bool betsClosed = false;
         uint storedBlockNumber;
         address trustedParty = 0xdCad3a6d3569DF655070DEd06cb7A1b2Ccd1D3AF;

         function setSealedSeed(bytes32 _sealedSeed) public {
             require(!seedSet);
             require (msg.sender == trustedParty);
             betsClosed = true;
             sealedSeed = _sealedSeed;
             storedBlockNumber = block.number + 1;
             seedSet = true;
         }

         function bet() public {
             require(!betsClosed);
             // Make bets here
         }

         function reveal(bytes32 _seed) public {
             require(seedSet);
             require(betMade);
             require(storedBlockNumber < block.number);
             require(keccak256(msg.sender, _seed) == sealedSeed);
             uint random = uint(keccak256(_seed, blockhash(storedBlockNumber)));
             // Insert logic for usage of random number here;
             seedSet = false;
             betsClosed = false;
         }
     }
     ```
   * **Pros:** Simple to implement.
   * **Cons:** Reveal should be done in the next 256 blocks.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

Consider implementing any of the suggested alternatives to generate the random numbers.

### Remediation Plan

**ACKNOWLEDGED:** The **WinWin team** acknowledged this issue and stated that the random number generation will be kept off-chain until oracle/rng becomes available in Pulsechain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | WinWin Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/winwin/winwin-protocol-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/winwin/winwin-protocol-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

