"""Behavioral protocols (ports) for lexique domain objects.

This package defines cross-cutting interfaces — display, glosing, segmentation,
YAML loading — not third-party integrations. Domain types in ``pfmg.lexique``
implement or mix in these protocols; ``pfmg.parsing`` may depend on
``pfmg.external.reader`` only.

Dependency rule: ``external`` may import ``pfmg.utils`` only, never ``lexique``.
"""
