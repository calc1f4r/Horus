---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4637
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-factorydao-contest
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: #l-01-missing-parameter-validations-in-speedbumppricegateaddgate

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-01] Missing parameter validations in 

### Overview

See description below for full details.

### Original Finding Content

<h2 id="l-01-missing-parameter-validations-in-speedbumppricegateaddgate" style="position:relative;"><a href="#l-01-missing-parameter-validations-in-speedbumppricegateaddgate" aria-label="l 01 missing parameter validations in speedbumppricegateaddgate permalink" class="anchor before"><svg aria-hidden="true" focusable="false" height="16" version="1.1" viewbox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>[L-01] Missing parameter validations in <code>SpeedBumpPriceGate#addGate</code></h2>
<p>Callers of <code>addGate</code> can create price gates with a zero price floor (allowing users to claim free tokens), and zero <code>priceIncreaseDenominator</code> (causing price calculation to revert with a divide by zero error).</p>
<p><a href="https://github.com/code-423n4/2022-05-factorydao/blob/e22a562c01c533b8765229387894cc0cb9bed116/contracts/SpeedBumpPriceGate.sol#L36-L45"><code>SpeedBumpPriceGate#addGate</code></a></p>
<pre class="grvsc-container dark-default-dark" data-language="solidity" data-index="32"><code class="grvsc-code"><span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">    </span><span class="mtk4">function</span><span class="mtk1"> </span><span class="mtk11">addGate</span><span class="mtk1">(</span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceFloor</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceDecay</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceIncrease</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1">, </span><span class="mtk12">address</span><span class="mtk1"> </span><span class="mtk12">beneficiary</span><span class="mtk1">) </span><span class="mtk11">external</span><span class="mtk1"> {</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk3">// prefix operator increments then evaluates</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">Gate</span><span class="mtk1"> </span><span class="mtk12">storage</span><span class="mtk1"> </span><span class="mtk12">gate</span><span class="mtk1"> = </span><span class="mtk12">gates</span><span class="mtk1">[++</span><span class="mtk12">numGates</span><span class="mtk1">];</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceFloor</span><span class="mtk1"> = </span><span class="mtk12">priceFloor</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">decayFactor</span><span class="mtk1"> = </span><span class="mtk12">priceDecay</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceIncreaseFactor</span><span class="mtk1"> = </span><span class="mtk12">priceIncrease</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1"> = </span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">beneficiary</span><span class="mtk1"> = </span><span class="mtk12">beneficiary</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">    }</span></span></span></code></pre>
<p>Suggestion: Validate that <code>priceFloor</code> and <code>priceIncreaseDenominator</code> are nonzero.</p>
<pre class="grvsc-container dark-default-dark" data-language="solidity" data-index="33"><code class="grvsc-code"><span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">    </span><span class="mtk4">function</span><span class="mtk1"> </span><span class="mtk11">addGate</span><span class="mtk1">(</span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceFloor</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceDecay</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceIncrease</span><span class="mtk1">, </span><span class="mtk12">uint</span><span class="mtk1"> </span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1">, </span><span class="mtk12">address</span><span class="mtk1"> </span><span class="mtk12">beneficiary</span><span class="mtk1">) </span><span class="mtk11">external</span><span class="mtk1"> {</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk11">require</span><span class="mtk1">(</span><span class="mtk12">priceFloor</span><span class="mtk1"> != </span><span class="mtk7">0</span><span class="mtk1">, </span><span class="mtk8">"Price floor must be nonzero"</span><span class="mtk1">);</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk11">require</span><span class="mtk1">(</span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1"> != </span><span class="mtk7">0</span><span class="mtk1">, </span><span class="mtk8">"Denominator must be nonzero"</span><span class="mtk1">);</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk3">// prefix operator increments then evaluates</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">Gate</span><span class="mtk1"> </span><span class="mtk12">storage</span><span class="mtk1"> </span><span class="mtk12">gate</span><span class="mtk1"> = </span><span class="mtk12">gates</span><span class="mtk1">[++</span><span class="mtk12">numGates</span><span class="mtk1">];</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceFloor</span><span class="mtk1"> = </span><span class="mtk12">priceFloor</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">decayFactor</span><span class="mtk1"> = </span><span class="mtk12">priceDecay</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceIncreaseFactor</span><span class="mtk1"> = </span><span class="mtk12">priceIncrease</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1"> = </span><span class="mtk12">priceIncreaseDenominator</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">        </span><span class="mtk12">gate</span><span class="mtk1">.</span><span class="mtk12">beneficiary</span><span class="mtk1"> = </span><span class="mtk12">beneficiary</span><span class="mtk1">;</span></span></span>
<span class="grvsc-line"><span class="grvsc-source"><span class="mtk1">    }</span></span></span></code></pre>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: #l-01-missing-parameter-validations-in-speedbumppricegateaddgate
- **Contest**: https://code4rena.com/contests/2022-05-factorydao-contest

### Keywords for Search

`vulnerability`

