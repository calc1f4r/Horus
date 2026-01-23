---
# Core Classification
protocol: generic
chain: everychain
category: cryptography
vulnerability_type: weak_randomness

# Attack Vector Details
attack_type: prediction
affected_component: random_number_generation

# Technical Primitives
primitives:
  - blockhash
  - block.timestamp
  - block.number
  - block.difficulty
  - prevrandao
  - keccak256
  - Chainlink_VRF
  - commit_reveal

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - defi
  - gaming
  - lottery
  - nft
  - randomness
  - real_exploit
  - DeFiHackLabs

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs
---

# Weak Randomness Vulnerabilities

## Overview

Weak randomness vulnerabilities occur when smart contracts use predictable or manipulable sources for generating random numbers. On-chain sources like `block.timestamp`, `blockhash`, `block.number`, and `prevrandao` can be predicted or influenced by miners/validators, making them unsuitable for high-stakes applications like lotteries, NFT minting, or gaming.

**Total Historical Losses from Analyzed Exploits: >$30M USD**

---

## Vulnerability Categories

### 1. Block Property Prediction
Using `block.timestamp`, `block.number`, `block.difficulty` as randomness.

### 2. Blockhash Manipulation
Exploiting `blockhash()` limitations and predictability.

### 3. Prevrandao (Post-Merge) Exploitation
Using `block.prevrandao` which is still somewhat predictable.

### 4. Same-Block Prediction
Attacker contracts can compute "random" values in the same block.

### 5. Commit-Reveal Bypass
Flawed implementations of commit-reveal schemes.

---

## Vulnerable Pattern Examples

### Example 1: Block Timestamp Randomness [CRITICAL]

**Real Exploit: Fomo3D and similar (2018+) - >$10M Lost**

```solidity
// ❌ VULNERABLE: Predictable randomness from block.timestamp
contract VulnerableLottery {
    mapping(uint256 => address) public tickets;
    uint256 public ticketCount;
    
    function buyTicket() external payable {
        require(msg.value == 0.1 ether, "Wrong price");
        tickets[ticketCount++] = msg.sender;
    }
    
    function pickWinner() external {
        require(ticketCount > 0, "No tickets");
        
        // @audit VULNERABLE: block.timestamp is known to miners
        // Miners can manipulate timestamp within ~15 second window
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,  // Or prevrandao post-merge
            ticketCount
        )));
        
        uint256 winnerIndex = random % ticketCount;
        address winner = tickets[winnerIndex];
        
        payable(winner).transfer(address(this).balance);
    }
}

// Attack vector:
// 1. Miner participates in lottery
// 2. Miner only includes their winning block if they win
// 3. Miner can try multiple timestamp values within valid range
```

---

### Example 2: Same-Block Prediction [CRITICAL]

**Real Exploit: LuckyTiger NFT (2022-07) - All Rare NFTs Stolen**

```solidity
// @PoC: DeFiHackLabs/src/test/2022-07/LuckyTiger_exp.sol
// ❌ VULNERABLE: Randomness computable in same transaction

contract LuckyTigerNFT {
    function mint() external payable {
        require(msg.value == 0.1 ether, "Wrong price");
        
        // @audit Attacker can compute this in same block before calling
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            msg.sender,
            totalSupply()
        )));
        
        uint256 rarity = random % 100;
        if (rarity < 5) {
            _mintLegendary(msg.sender);
        } else if (rarity < 20) {
            _mintRare(msg.sender);
        } else {
            _mintCommon(msg.sender);
        }
    }
}

// Attack contract:
contract NFTExploit {
    LuckyTigerNFT public target;
    
    function exploit() external payable {
        // Pre-compute the "random" value
        uint256 predictedRandom = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            address(this),
            target.totalSupply()
        )));
        
        uint256 predictedRarity = predictedRandom % 100;
        
        // Only mint if we'll get a rare NFT
        require(predictedRarity < 5, "Not legendary, reverting");
        
        target.mint{value: 0.1 ether}();
    }
    
    // Call this repeatedly until it succeeds
    function tryMint() external payable {
        try this.exploit{value: msg.value}() {
            // Success - got rare NFT
        } catch {
            // Not rare, try again next block
        }
    }
}
```

---

### Example 3: Blockhash Vulnerability [HIGH]

**Real Exploit: Multiple Gambling DApps**

```solidity
// ❌ VULNERABLE: blockhash has limitations

contract VulnerableGambling {
    struct Bet {
        address player;
        uint256 amount;
        uint256 blockNumber;
    }
    
    mapping(uint256 => Bet) public bets;
    uint256 public betId;
    
    function placeBet() external payable {
        bets[betId++] = Bet(msg.sender, msg.value, block.number);
    }
    
    function resolveBet(uint256 _betId) external {
        Bet memory bet = bets[_betId];
        require(bet.blockNumber < block.number, "Too early");
        
        // @audit BUG 1: blockhash returns 0 for blocks > 256 blocks old
        // Attacker can wait 256+ blocks and get predictable 0 hash
        bytes32 hash = blockhash(bet.blockNumber);
        
        // @audit BUG 2: Even for recent blocks, miners know blockhash
        // before including bet placement transaction
        
        uint256 random = uint256(hash) % 2;
        
        if (random == 1) {
            payable(bet.player).transfer(bet.amount * 2);
        }
    }
}

// Attack: Wait 256+ blocks, blockhash returns 0
// uint256(0) % 2 = 0, so attacker always loses? 
// Or if contract checks for 0 hash but has fallback logic, exploit that
```

---

### Example 4: Prevrandao Misconception [HIGH]

**Post-Merge Ethereum (2022+)**

```solidity
// ❌ VULNERABLE: prevrandao is not truly random
contract PostMergeVulnerable {
    function getRandomNumber() public view returns (uint256) {
        // @audit prevrandao (formerly difficulty) is known to validators
        // Validators can choose not to propose a block if result unfavorable
        // While harder to manipulate than pre-merge, still not secure
        return uint256(keccak256(abi.encodePacked(
            block.prevrandao,
            block.timestamp,
            msg.sender
        )));
    }
}

// Issues with prevrandao:
// 1. Known 1 epoch (~6.4 minutes) in advance
// 2. Validators can skip their slot (lose rewards) to avoid unfavorable randomness
// 3. Still deterministic for same-block exploitation
```

---

### Example 5: Flawed Commit-Reveal [MEDIUM]

**Real Exploit Pattern: Multiple NFT/Game Projects**

```solidity
// ❌ VULNERABLE: Incomplete commit-reveal implementation

contract FlawedCommitReveal {
    mapping(address => bytes32) public commits;
    mapping(address => bool) public revealed;
    
    function commit(bytes32 _hash) external {
        // @audit No time lock - can reveal in same block
        commits[msg.sender] = _hash;
    }
    
    function reveal(uint256 _secret, uint256 _choice) external {
        bytes32 expectedHash = keccak256(abi.encodePacked(_secret, _choice));
        require(commits[msg.sender] == expectedHash, "Invalid reveal");
        require(!revealed[msg.sender], "Already revealed");
        
        revealed[msg.sender] = true;
        
        // @audit Attacker can see other reveals in mempool
        // and front-run with their own strategic reveal
        
        processChoice(msg.sender, _choice);
    }
}

// ✅ SECURE: Proper commit-reveal with time locks
contract SecureCommitReveal {
    struct Commitment {
        bytes32 hash;
        uint256 commitBlock;
        bool revealed;
    }
    
    mapping(address => Commitment) public commits;
    uint256 public constant REVEAL_DELAY = 10; // blocks
    uint256 public constant REVEAL_WINDOW = 50; // blocks
    
    function commit(bytes32 _hash) external {
        require(commits[msg.sender].commitBlock == 0, "Already committed");
        commits[msg.sender] = Commitment(_hash, block.number, false);
    }
    
    function reveal(uint256 _secret, uint256 _choice) external {
        Commitment storage c = commits[msg.sender];
        require(c.commitBlock > 0, "No commitment");
        require(!c.revealed, "Already revealed");
        require(block.number >= c.commitBlock + REVEAL_DELAY, "Too early");
        require(block.number <= c.commitBlock + REVEAL_DELAY + REVEAL_WINDOW, "Too late");
        
        bytes32 expectedHash = keccak256(abi.encodePacked(_secret, _choice));
        require(c.hash == expectedHash, "Invalid reveal");
        
        c.revealed = true;
        processChoice(msg.sender, _choice);
    }
}
```

---

### Example 6: RND Token Exploit [HIGH]

**Real Exploit: RND Token (2023-03) - $9K Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2023-03/RND_exp.sol
// ❌ VULNERABLE: Lottery with predictable randomness

contract RNDLottery {
    function spin() external payable {
        require(msg.value >= minBet, "Bet too low");
        
        // @audit All inputs are predictable or controllable
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.number,
            msg.sender,
            tx.gasprice,  // Even gas price is controllable by attacker
            address(this).balance
        )));
        
        uint256 result = random % 100;
        
        if (result < 10) {
            // Jackpot!
            payable(msg.sender).transfer(address(this).balance);
        }
    }
}
```

---

## Real-World Exploits Summary

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| Fomo3D | 2018-08 | >$3M | Block manipulation |
| LuckyTiger | 2022-07 | NFTs | Same-block prediction |
| RND Token | 2023-03 | $9K | Predictable inputs |
| Multiple Lotteries | Various | >$20M | Weak randomness |
| NFT Mints | Various | Rare NFTs | Same-block prediction |

---

## Secure Implementation Guidelines

### 1. Use Chainlink VRF
```solidity
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract SecureLottery is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface COORDINATOR;
    uint64 s_subscriptionId;
    bytes32 keyHash;
    
    mapping(uint256 => address) public requestToPlayer;
    
    function requestRandomWinner() external returns (uint256 requestId) {
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            3,  // confirmations
            100000,  // callback gas
            1   // numWords
        );
        requestToPlayer[requestId] = msg.sender;
    }
    
    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomWords
    ) internal override {
        // This is called by Chainlink with verifiable randomness
        uint256 winnerIndex = randomWords[0] % participantCount;
        // ... select winner
    }
}
```

### 2. Proper Commit-Reveal
```solidity
contract ProperCommitReveal {
    uint256 public constant COMMIT_PERIOD = 100; // blocks
    uint256 public constant REVEAL_PERIOD = 100; // blocks
    
    mapping(address => bytes32) public commits;
    mapping(address => uint256) public commitBlocks;
    bytes32 public combinedRandomness;
    
    function commit(bytes32 hash) external {
        require(isCommitPhase(), "Not commit phase");
        commits[msg.sender] = hash;
        commitBlocks[msg.sender] = block.number;
    }
    
    function reveal(bytes32 secret) external {
        require(isRevealPhase(), "Not reveal phase");
        require(keccak256(abi.encode(secret)) == commits[msg.sender], "Bad reveal");
        
        // Combine all revealed secrets
        combinedRandomness = keccak256(abi.encode(combinedRandomness, secret));
    }
}
```

### 3. Use Block Hash from Future Block (with timeout)
```solidity
contract FutureBlockRandom {
    struct Request {
        uint256 targetBlock;
        address requester;
    }
    
    mapping(uint256 => Request) public requests;
    uint256 public requestId;
    
    function requestRandom() external returns (uint256) {
        uint256 id = requestId++;
        // Target block is in the future
        requests[id] = Request(block.number + 10, msg.sender);
        return id;
    }
    
    function fulfillRandom(uint256 id) external view returns (uint256) {
        Request memory r = requests[id];
        require(block.number > r.targetBlock, "Too early");
        require(block.number <= r.targetBlock + 256, "Too late, use backup");
        
        bytes32 hash = blockhash(r.targetBlock);
        require(hash != 0, "Block too old");
        
        return uint256(keccak256(abi.encode(hash, id)));
    }
}
```

---

## Detection Patterns

### Semgrep Rules
```yaml
rules:
  - id: weak-randomness-blockhash
    patterns:
      - pattern-either:
          - pattern: blockhash(...)
          - pattern: block.timestamp
          - pattern: block.number
          - pattern: block.difficulty
          - pattern: block.prevrandao
      - pattern-inside: |
          function $FUNC(...) ... {
              ... keccak256(...) ...
          }
    message: "Potential weak randomness using block properties"
    severity: WARNING
```

### Manual Checklist
- [ ] Is randomness needed for high-value decisions?
- [ ] Are any block properties (timestamp, number, prevrandao) used?
- [ ] Can an attacker contract predict the "random" value?
- [ ] Is there a commit-reveal scheme with proper time locks?
- [ ] Is Chainlink VRF or similar oracle used?
- [ ] Can miners/validators influence the outcome?

---

## Keywords for Search

`randomness`, `random number`, `block.timestamp`, `blockhash`, `block.number`, `block.difficulty`, `prevrandao`, `keccak256`, `lottery`, `gambling`, `commit reveal`, `VRF`, `Chainlink VRF`, `predictable`, `NFT rarity`, `gaming`, `raffle`
