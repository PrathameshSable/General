#!/usr/bin/env python3
"""Run a Fabric notebook from notebooks/ locally on PySpark + Delta, with shims for the Fabric runtime.

Lets notebooks 00–03 be tested outside Fabric against a folder that mimics a Lakehouse
(<root>/Tables/<schema>/<table>/_delta_log, <root>/Files/...). Notebook 04 needs Fabric (Semantic Link).

Usage:
    python -m venv .venv && .venv/bin/pip install "pyspark==3.5.1" "delta-spark==3.2.0"
    .venv/bin/python scripts/run_notebook_local.py notebooks/00_generate_sample_data.ipynb
    .venv/bin/python scripts/run_notebook_local.py notebooks/01_lakehouse_data_profiling.ipynb RELATIONSHIP_SCAN_MODE=all
    .venv/bin/python scripts/run_notebook_local.py notebooks/02_logical_model_design.ipynb
    .venv/bin/python scripts/run_notebook_local.py notebooks/03_build_dim_fact_model.ipynb

Options:
    --root <dir>   fake lakehouse folder (default: outputs/fake_lakehouse)
    KEY=VALUE      override any variable from the notebook's tagged `parameters` cell
"""
import json, os, sys, types
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
root = str(REPO / "outputs" / "fake_lakehouse")
if "--root" in args:
    i = args.index("--root")
    root = os.path.abspath(args[i + 1])
    del args[i:i + 2]
if not args:
    sys.exit(__doc__)
nb_path, overrides = Path(args[0]), dict(a.split("=", 1) for a in args[1:])
os.makedirs(os.path.join(root, "Tables"), exist_ok=True)
os.makedirs(os.path.join(root, "Files"), exist_ok=True)

from pyspark.sql import SparkSession  # noqa: E402
from delta import configure_spark_with_delta_pip  # noqa: E402

builder = (SparkSession.builder.master("local[2]").appName(nb_path.stem)
           .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
           .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
           .config("spark.sql.shuffle.partitions", "4").config("spark.ui.enabled", "false")
           .config("spark.sql.warehouse.dir", os.path.join(root, "_warehouse")))
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


class _Entry:
    def __init__(self, path):
        self.path, self.name = path, os.path.basename(path.rstrip("/"))
        self.isDir = os.path.isdir(path)
        self.isFile = not self.isDir
        self.size = 0 if self.isDir else os.path.getsize(path)


class _FS:
    @staticmethod
    def ls(path):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return [_Entry(os.path.join(path, n)) for n in sorted(os.listdir(path))]

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def mkdirs(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def put(path, content, overwrite=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Path(path).write_text(content)

    @staticmethod
    def head(path, max_bytes=1 << 20):
        return Path(path).read_text()[:max_bytes]


class _Runtime:
    context = {"defaultLakehouseWorkspaceId": "local-ws", "defaultLakehouseId": "local-lh", "defaultLakehouseName": "LocalLakehouse",
               "currentWorkspaceId": "local-ws", "currentNotebookName": nb_path.stem}


notebookutils = types.SimpleNamespace(fs=_FS, runtime=_Runtime)


def display(df):
    try:
        df.show(20, truncate=60)
    except Exception:
        print(df)


def _literal(v):
    if v in ("True", "False"):
        return v
    try:
        float(v)
        return v
    except ValueError:
        return repr(v)


nb = json.loads(nb_path.read_text())
g = {"spark": spark, "notebookutils": notebookutils, "display": display, "__name__": "__main__"}
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    if src.lstrip().startswith("%"):
        print(f"[cell {i}] skipping magic: {src.strip().splitlines()[0]}")
        continue
    if "parameters" in cell["metadata"].get("tags", []):
        src += "\nLAKEHOUSE_ROOT = %r\n" % root + "\n".join(f"{k} = {_literal(v)}" for k, v in overrides.items())
    print(f"\n===== {nb_path.name} [cell {i}] =====")
    exec(compile(src, f"{nb_path.stem}_cell{i}", "exec"), g)
spark.stop()
print(f"\n{nb_path.name}: all cells executed")
