"""
Explainability Subsystem for ELIZA.
Enforces Article XIII: Every decision must answer Why?, Based on what evidence?, Which beliefs?, Which assumptions?, Which alternatives?, How confident?.
"""

from eliza.explainability.tracer import ExplainabilityTracer

__all__ = ["ExplainabilityTracer"]
