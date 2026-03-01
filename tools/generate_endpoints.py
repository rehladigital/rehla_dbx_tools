"""Generate endpoint modules from an endpoint catalog.

Usage:
    py tools/generate_endpoints.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "src" / "databricks_api" / "endpoints" / "generated"
CATALOG_PATH = ROOT / "src" / "databricks_api" / "endpoints" / "catalog.py"


TEMPLATE_HEADER = '''"""Auto-generated endpoint constants.

Do not edit manually; regenerate with tools/generate_endpoints.py
"""
'''


def main() -> None:
    endpoint_catalog = _load_catalog()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "__init__.py").write_text('"""Generated endpoint constants."""\n', encoding="utf-8")

    for scope, versions in endpoint_catalog.items():
        lines = [TEMPLATE_HEADER, ""]
        for version, endpoints in versions.items():
            const_name = f"{scope.upper()}_{version.replace('.', '_').upper()}_ENDPOINTS"
            lines.append(f"{const_name} = {{")
            for key, value in sorted(endpoints.items()):
                lines.append(f'    "{key}": "{value}",')
            lines.append("}")
            lines.append("")
        target = OUT_DIR / f"{scope}_endpoints.py"
        target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"Generated {target}")


def _load_catalog() -> dict:
    spec = importlib.util.spec_from_file_location("endpoint_catalog_module", CATALOG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load catalog module from {CATALOG_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "ENDPOINT_CATALOG")


if __name__ == "__main__":
    main()
