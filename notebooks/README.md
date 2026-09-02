# Fabric Lakehouse → Star Schema → Semantic Model notebooks

A five-step, parameter-driven notebook pipeline for Microsoft Fabric that takes an unfamiliar Lakehouse and
turns it into a documented dimensional model wired to a Direct Lake semantic model.

```
 Lakehouse tables ──► 01 profile ──► 02 logical model ──► 03 gold dim/fact ──► 04 semantic model
                        │                │                     │                    │
                        ▼                ▼                     ▼                    ▼
                  profiling.*      Files/model/           gold.dim_* /        Direct Lake model
                  Delta tables     model_spec.json        gold.fact_*         + .bim export
                                   review .md + .mmd      + validation table
```

| Notebook | Purpose | Reads | Writes |
|---|---|---|---|
| `00_generate_sample_data` | *Optional.* Synthetic retail data (with duplicate keys, orphans, nulls) to trial the pipeline | — | `bronze.*` |
| `01_lakehouse_data_profiling` | Table / column statistics, semantic roles, candidate keys, relationship discovery by name + value containment | every Delta table under `Tables/` | `profiling.table_profile`, `column_profile`, `relationship_candidates`, `profiling_runs` |
| `02_logical_model_design` | Classifies fact / dimension / bridge, picks natural keys, flattens snowflakes, role-plays dates, proposes measures; bus matrix + Mermaid ER diagram | `profiling.*` | `Files/model/model_spec.json`, `logical_model_review.md`, `model_spec.mmd` |
| `03_build_dim_fact_model` | Materialises `dim_date`, `dim_*` (surrogate keys, Unknown member, optional SCD2), `fact_*` (SK lookups, date keys, header→line inheritance); validation table | sources + `model_spec.json` | `gold.dim_*`, `gold.fact_*`, `gold.gold_build_validation` |
| `04_semantic_model_deploy` | Creates the Direct Lake semantic model with Semantic Link Labs: relationships, date table, hidden keys, hierarchies, measures, refresh, DAX smoke test, `.bim` export | `gold.*` + `model_spec.json` | Semantic model in the workspace, `Files/model/<model>.bim` |
| `05_run_pipeline` | Runs 01→04 with shared parameters via `notebookutils.notebook.run` | — | — |

## Quick start

1. In a Fabric workspace, **Import notebook** → upload the six `.ipynb` files.
2. Open `01_lakehouse_data_profiling`, attach the Lakehouse you want to understand as the **default Lakehouse**
   (or set `LAKEHOUSE_ROOT` to an `abfss://` path), and **Run all**. Read the summary tables at the bottom.
3. Run `02_logical_model_design`. Read the printed review: bus matrix, notes, unresolved items. Fix decisions with
   `TABLE_ROLE_OVERRIDES` / `NATURAL_KEY_OVERRIDES` and re-run, or edit `Files/model/model_spec.json` by hand.
4. Run `03_build_dim_fact_model`. Every table gets reconciled (row counts, key uniqueness, orphans, date coverage) and the
   notebook fails loudly if a check fails.
5. Run `04_semantic_model_deploy`. Open the semantic model in the workspace and start building reports.
6. Once settled, schedule `05_run_pipeline` or wire the four notebooks into a Data Factory pipeline.

No client data? Run `00_generate_sample_data` first; the whole pipeline works on it out of the box.

## Design decisions worth knowing

- **Path-based discovery.** Tables are found by walking `Tables/` (and `Tables/<schema>/`), so the notebooks work on
  schema-enabled and classic Lakehouses alike and never depend on the Spark catalog's naming of lakehouses.
- **One aggregation pass per table.** Profiling scales to large tables; distinct counts switch to HyperLogLog above
  `MAX_ROWS_FOR_EXACT` rows. Relationship checks are one semi-join per name-matched pair
  (`RELATIONSHIP_SCAN_MODE = "all"` checks every type-compatible pair when column names are unhelpful).
- **Row-weighted containment.** A relationship is accepted when ≥ 95 % of child *rows* find a parent, so a few orphan rows
  (late-arriving or deleted parents) do not hide a real relationship. Orphans map to the **Unknown member (-1)** in gold.
- **Near-unique parents.** A dimension source with a few duplicate key rows still acts as a parent; the build de-duplicates
  (most populated row wins) and the review flags it for confirmation with the data owner.
- **Header/line pattern.** A fact that references another fact (`order_items → orders`) inherits the header's dimension and
  date keys so line-level measures can be sliced by customer, store, order date, etc.
- **Snowflakes are flattened** into the child dimension (`dim_store` absorbs `regions`), which is what Direct Lake and
  Power BI users want. Set `FLATTEN_SNOWFLAKES = False` to keep them separate.
- **Role-playing dates.** Every fact date column becomes a `<role>_date_key` relationship to one `dim_date`; the first is
  active, the others inactive with a ready-made `USERELATIONSHIP` measure.
- **Everything is a parameter.** Each notebook has a tagged `parameters` cell, so a pipeline Notebook activity or
  `notebookutils.notebook.run` can drive it.
- **Source-of-truth.** Nothing is invented: every model decision traces to a profiled statistic or an explicit override,
  and `model_spec.json` records the profiling `run_id` it was derived from.

## `model_spec.json` at a glance

```jsonc
{
  "model_name": "Lakehouse Model",
  "gold_schema": "gold",
  "date_dimension": {"name": "dim_date", "start": "2023-01-01", "end": "2026-12-31", "fiscal_year_start_month": 1},
  "dimensions": [{"name": "dim_customer", "source_table": "customers", "natural_key": ["customer_id"],
                  "surrogate_key": "customer_key", "attributes": ["first_name", "..."], "scd_type": 1,
                  "snowflake_parents": []}],
  "facts": [{"name": "fact_order_items", "source_table": "order_items", "grain": "one row per order_items row",
             "foreign_keys": [{"column": "product_id", "dimension": "dim_product", "surrogate_key_column": "product_key",
                               "role": "", "inherited_from": null}],
             "date_columns": [{"column": "order_date", "date_key_column": "order_date_key", "role": "order", "active": true}],
             "measures": [{"column": "line_total", "aggregation": "sum", "measure_name": "Total Line Total", "format_string": "#,##0.00"}],
             "degenerate_columns": ["order_item_id", "order_id"], "header_links": []}],
  "bus_matrix": [], "notes": [], "unresolved": [], "mermaid": "erDiagram ..."
}
```

Edit it freely between steps 02 and 03: rename dimensions, drop attributes, change `scd_type`, add measures, or delete a
fact you do not want. Notebooks 03 and 04 only read the spec.

## Requirements

- Fabric Spark runtime 1.3 (Spark 3.5, Delta 3.x). Notebooks 01–03 use only PySpark and Delta.
- Notebook 04 installs `semantic-link-labs` (≥ 0.17) and needs Contributor on the target workspace.
- Direct Lake over OneLake is the default connection mode; set `USE_SQL_ENDPOINT = True` for SQL-endpoint mode.

## Validation status

Notebooks 00–03 were executed end-to-end locally on PySpark 3.5.1 + Delta 3.2 against the synthetic dataset (schema-enabled
layout), with all 21 gold build checks passing. Notebook 04 relies on the Fabric runtime (Semantic Link and the workspace
XMLA endpoint) and was validated by syntax check and against the installed `semantic-link-labs` 0.17 API signatures; run it
inside Fabric to confirm end-to-end.
