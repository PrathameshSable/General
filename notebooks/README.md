# Notebooks

## `semantic_model_recommender.ipynb` — AI-recommended semantic model from lakehouse tables

A Microsoft Fabric notebook that looks at the Delta tables in a lakehouse and uses an LLM to
recommend a Power BI semantic model, then generates it as a **Direct Lake** model (TMDL) and can
deploy it to the workspace.

### What it does

| Step | Cell | What happens |
|---|---|---|
| Profile | 3 | Row counts, cardinality, null rates, min/max, candidate keys, sample values per table (sampled, bounded by `SAMPLE_ROWS`) |
| Relationship candidates | 4 | Name matching (`customer_id` → `dim_customer.customer_id`) confirmed by value overlap between tables |
| Role hints | 5 | Fact vs dimension heuristics (prefixes, FK count, numeric measure columns) |
| LLM recommendation | 7 | Sends the profile + business context and asks for a JSON recommendation: tables to include/exclude, display names, hidden columns, relationships, DAX measures, date dimension, warnings, open questions |
| Validation | 8 | Drops anything the LLM invented (tables, columns, relationships), flags relationship type mismatches and unknown DAX references |
| Date dimension | 9 | Optionally creates a `dim_date` Delta table (Direct Lake cannot use DAX calculated tables) and wires the fact date columns to it |
| Summary | 10 | Markdown report of the recommended model |
| TMDL | 11 | Generates `definition.pbism`, `model.tmdl`, `database.tmdl`, `expressions.tmdl`, `relationships.tmdl`, `tables/*.tmdl` |
| Write | 12 | Writes the report, profile, and `<Model>.SemanticModel/` folder to `Files/semantic_model_recommendations/` in the lakehouse |
| Deploy | 13 | Optional: creates or updates the semantic model in the workspace via the Fabric REST API |

### LLM options (`LLM_PROVIDER`)

- `fabric_openai` — Azure OpenAI built into Fabric. No key. Requires a capacity with Copilot/AI enabled (F64+ or equivalent) and the tenant setting on.
- `azure_openai` — your own Azure OpenAI resource. Set `AZURE_OPENAI_ENDPOINT` and a key (inline or Key Vault).
- `anthropic` — Claude via the Anthropic API. Set `LLM_MODEL` to e.g. `claude-sonnet-5` and a key (inline or Key Vault).

Only metadata, statistics, and up to five sample values per column are sent to the model. Set
`SEND_SAMPLE_VALUES = False` to send schema and statistics only.

### How to use

1. Import the `.ipynb` into a Fabric workspace and attach the lakehouse as the default lakehouse
   (or set `LAKEHOUSE_NAME`).
2. Fill in the configuration cell: provider, model, `BUSINESS_CONTEXT` (what the data is, key KPIs).
3. Run all cells with `DEPLOY_TO_WORKSPACE = False` and review the summary and warnings.
4. Fix anything flagged in the lakehouse (for example a relationship type mismatch, or a timestamp
   column that needs a date-typed twin), rerun, then set `DEPLOY_TO_WORKSPACE = True`.
5. Open the deployed model, run a quick `EVALUATE { [Total Sales] }` style check, then add RLS,
   hierarchies, and calculation groups in Desktop or web modeling.

### Direct Lake modes

- `onelake` (default): the model reads Delta tables from OneLake directly, compatibility level 1702.
- `sql_endpoint`: the classic Direct Lake over the lakehouse SQL analytics endpoint, compatibility
  level 1604. The notebook resolves the endpoint connection string from the Fabric API.

### Requirements

- Workspace role: Contributor or higher to deploy.
- Python packages available in the Fabric runtime: `openai`, `synapse.ml`, `requests`. The
  `anthropic` package is pip-installed on demand.
