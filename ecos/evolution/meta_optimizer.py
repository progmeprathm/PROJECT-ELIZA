"""
Layer 8 & 9: Meta-Cognitive Optimizer and Architecture Optimizer.
"""

from typing import Any, Dict, List

from ecos.benchmarks.evaluator import CognitiveEvaluationResult


class MetaCognitiveOptimizer:
    """
    Layer 8: Reasons about cognitive process parameter tuning.
    Answers: Which reasoning style worked best? Was simulation depth optimal? Should attention allocation change?
    """

    def optimize_process_parameters(self, eval_results: List[CognitiveEvaluationResult]) -> Dict[str, Any]:
        avg_score = sum(e.overall_score for e in eval_results) / len(eval_results) if eval_results else 0.5

        recommendations = {
            "optimal_reasoning_style": "deductive" if avg_score > 0.8 else "probabilistic",
            "recommended_simulation_depth": 3 if avg_score > 0.85 else 5,
            "attention_allocation_multiplier": 1.2 if avg_score < 0.7 else 1.0,
            "aggregate_performance": round(avg_score, 4),
        }
        return recommendations


class ArchitectureOptimizer:
    """
    Layer 9: Evidence-based benchmarking and replacement of cognitive modules (e.g. Planner A vs Planner B).
    """

    def compare_modules(self, module_a_name: str, score_a: float, module_b_name: str, score_b: float) -> Dict[str, Any]:
        winner = module_a_name if score_a >= score_b else module_b_name
        return {
            "winner": winner,
            "module_a": {"name": module_a_name, "score": score_a},
            "module_b": {"name": module_b_name, "score": score_b},
            "performance_delta": round(abs(score_a - score_b), 4),
        }
