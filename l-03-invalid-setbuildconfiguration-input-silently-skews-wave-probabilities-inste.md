---
# Core Classification
protocol: Tollanuniverse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64100
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/TollanUniverse-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-03] Invalid `setBuildConfiguration()` Input Silently Skews Wave Probabilities Instead of Reverting

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `setBuildConfiguration()` allows a wave configuration where `config.waves[i].length` exceeds `elementIds.length`, as long as total probabilities sum to `10_000`. While validation passes, `_handleRandom()` later caps the rolled `count` to `elemCount`, silently increasing the probability of the highest valid count.

### Root cause

The `setBuildConfiguration()` validates `config.waves[i][j].count` is within [1, 4], but does not enforce  
`config.waves[i].length == elementIds.length`.

In `_handleRandom()`, rolls resolving to an invalid higher count are capped:

```solidity
if (count > elemCount) count = elemCount;
```

## Location of Affected Code

File: [contracts/TollanRandomConsumerMax.sol](https://github.com/TollanWorlds/tollan-rng-smart-contract/blob/afacb9a2f31a0b4a38a7e72b915fed5937cf27eb/contracts/TollanRandomConsumerMax.sol)

## Impact

A misconfigured build does not revert and instead affects randomness, increasing the probability of rolling the highest possible count and altering wave outcomes.

### Example

For `elemCount = 3` and wave config:

```json
[
  { "count": 1, "chance": 2500 },
  { "count": 2, "chance": 2500 },
  { "count": 3, "chance": 2500 },
  { "count": 4, "chance": 2500 }
]
```

The effective probability becomes:

```json
[
  { "count": 1, "chance": 2500 },
  { "count": 2, "chance": 2500 },
  { "count": 3, "chance": 5000 }
]
```

## Proof of Concept

Add the following test inside `TollanRandomConsumerMax.test.ts`:

```typescript
it("invalid setBuildConfiguration input does not fail but incorrectly increases probability for count 3", async () => {
  // ============================== START HELPER FUNCTIONS ==============================
  const MASK_256 = (1n << 256n) - 1n;

  const splitMixZWave0 = (randomNumber: bigint) => {
    let state = randomNumber & MASK_256;
    state = (state + 0x9e3779b97f4a7c15n) & MASK_256;
    let z = state;
    z = ((z ^ (z >> 30n)) * 0xbf58476d1ce4e5b9n) & MASK_256;
    z = ((z ^ (z >> 27n)) * 0x94d049bb133111ebn) & MASK_256;
    z = (z ^ (z >> 31n)) & MASK_256;
    return z;
  };

  const rollForSeedWave0 = (seed: bigint) =>
    Number(splitMixZWave0(seed) % 10000n);

  const findSeedInRollRange = (minIncl: number, maxIncl: number) => {
    for (let seed = 1n; seed < 200000n; seed++) {
      const roll = rollForSeedWave0(seed);
      if (roll >= minIncl && roll <= maxIncl) return seed;
    }
    throw new Error(
      `No seed found for roll range [${minIncl}, ${maxIncl}] in search bound`
    );
  };

  // ============================== END HELPER FUNCTIONS ==============================

  // 1. Configure wave distribution for 4 elements
  const { consumer, mockVrf } = await loadFixture(deployFixture);
  const waveWithAllCounts = [
    [
      { count: 1, chance: 2500 },
      { count: 2, chance: 2500 },
      { count: 3, chance: 2500 },
      { count: 4, chance: 2500 },
    ],
  ];

  //2. Configure 2 builds - 1 with only 3 elementIds, 2 with 4 elementIds
  const buildWith3Elements = 1;
  const buildWith4Elements = 2;
  await consumer.setBuildConfiguration(buildWith3Elements, {
    elementIds: [100, 101, 102],
    waves: waveWithAllCounts,
  });
  await consumer.setBuildConfiguration(buildWith4Elements, {
    elementIds: [100, 101, 102, 103],
    waves: waveWithAllCounts,
  });

  // 3. Find a random number such that roll falls into last 25% bucket: count=4 when roll in [7500..9999]
  const seedThatSelectsCount4 = findSeedInRollRange(7500, 9999);
  const roll = rollForSeedWave0(seedThatSelectsCount4);
  // Sanity: prove it's actually in the count=4 bucket
  expect(roll).to.be.greaterThanOrEqual(7500);
  expect(roll).to.be.lessThanOrEqual(9999);

  // 4. Request randomness for both builds
  await consumer.requestRandom(buildWith3Elements); // requestId 1
  await consumer.requestRandom(buildWith4Elements); // requestId 2

  // 5. Fulfill random numbers and extract waves
  const extractGeneratedWavesFromReceipt = async (tx: any) => {
    const receipt = await tx.wait();
    const log = receipt?.logs.find((l: any) => {
      try {
        return consumer.interface.parseLog(l)?.name === "ResultGeneratedIDs";
      } catch {
        return false;
      }
    });
    const parsed = consumer.interface.parseLog(log as any);
    return parsed.args.all as any; // uint8[][]
  };
  const generatedWavesElem3 = await extractGeneratedWavesFromReceipt(
    await mockVrf.fulfillRandomNumber(1, seedThatSelectsCount4)
  );
  const generatedWavesElem4 = await extractGeneratedWavesFromReceipt(
    await mockVrf.fulfillRandomNumber(2, seedThatSelectsCount4)
  );

  //6. Validate that a roll falling in [t3;t4) returns 3 due to cap check
  expect(generatedWavesElem3[0].length).to.equal(3); // capped from 4 -> 3
  expect(generatedWavesElem4[0].length).to.equal(4); // no cap, true count=4
});
```

## Recommendation

Validate at configuration time that no wave defines probabilities for selecting more elements than exist in the build (i.e., enforce `count <= elementIds.length`). This prevents silent probability folding at runtime and ensures the configured distribution matches the actual element set.

Add the following check inside the per-wave loop in `setBuildConfiguration()`:

```diff
function setBuildConfiguration(uint256 buildId, BuildConfiguration calldata config) external onlyOwner {
    require(buildId != 0, "Zero buildId");
    require(config.elementIds.length > 0 && config.elementIds.length <= 4, "Elements 1-4");
    require(config.waves.length > 0 && config.waves.length <= 64, "Waves 1-64");

    configs[buildId] = Config(uint8(config.waves.length), uint8(config.elementIds.length));

    uint256 slotsNeeded = (config.waves.length + 4) / 5;
    uint256[] memory packed = new uint256[](slotsNeeded);

    for (uint256 i = 0; i < config.waves.length; i++) {
        WaveConfiguration[] calldata opts = config.waves[i];
+       require(opts.length <= config.elementIds.length, "Opts count higher than elementIds size");
        uint16[5] memory chances;
        uint256 total = 0;

        for (uint256 j = 0; j < opts.length; j++) {
            uint8 cnt = opts[j].count;
            require(cnt >= 1 && cnt <= 4, "Count 1-4");
            require(chances[cnt] == 0, "Duplicate");
            chances[cnt] = opts[j].chance;
            total += opts[j].chance; }
        require(total == 10000, "Sum 10000");

        uint256 t1 = chances[1];
        uint256 t2 = t1 + chances[2];
        uint256 t3 = t2 + chances[3];

        packed[i / 5] |= ((t1 | (t2 << 16) | (t3 << 32)) << ((i % 5) * 48)); }

    delete packedWaves[buildId];
    for (uint256 i = 0; i < packed.length; i++) {
        packedWaves[buildId].push(packed[i]);
    }
}
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Tollanuniverse |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/TollanUniverse-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

