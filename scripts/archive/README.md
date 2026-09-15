# Archived Scripts

One-shot generators and fetchers whose output corpus is already committed to the
repository. They are retained for provenance and reproducibility, not for routine
use — nothing in the pipeline, CI, or the agent playbooks calls them.

| Script | Produced | Superseded by |
|--------|----------|---------------|
| `classify_cosmos.py` | Cosmos report classification buckets | `DB/cosmos/`, `DB/manifests/cosmos.json` |
| `generate_cosmos_entries.py` | First-pass Cosmos DB entries | `DB/cosmos/` |
| `generate_cosmos_v2.py` | Second-pass Cosmos DB entries | `DB/cosmos/` |
| `download_ottersec_move.py` | OtterSec Move audit PDFs | `reports/ottersec_move_audits/` |

Re-running any of these will overwrite curated content. Regenerate the DB through
`scripts/generate_manifests.py` instead; author new entries against `TEMPLATE.md`.
