"""Compatibility wrapper for the question-generation engine.

The supported public import surface remains ``pasuk_flow_generator.py``.
Internal implementation now lives under ``engine/``.
"""

import sys

from engine import flow_builder as _flow_builder

sys.modules[__name__] = _flow_builder


if __name__ == "__main__":
    _flow_builder.write_examples()
