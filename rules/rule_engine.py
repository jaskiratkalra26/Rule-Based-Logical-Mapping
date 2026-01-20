import inspect
from typing import Any, Dict, List, Optional, Union
from . import rule_functions
from .rule_metadata import RULE_METADATA

class RuleEngine:
    """
    Engine to execute logical mapping rules defined in rule_metadata and implemented in rule_functions.
    """

    def __init__(self):
        # Map rule_id to rule definition
        self.metadata = {r['rule_id']: r for r in RULE_METADATA}

    def _get_function(self, function_name: str):
        """Retrieves the callable function from rule_functions module."""
        if hasattr(rule_functions, function_name):
            return getattr(rule_functions, function_name)
        raise ValueError(f"Function '{function_name}' not found in rule_functions module.")

    def apply_rule(self, rule_id: str, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Applies a single rule by ID to the input data.

        Args:
            rule_id: The ID of the rule to apply (e.g., 'R1', 'R5').
            input_data: The text or data to process.
            context: Dictionary of runtime arguments (e.g., {'tokenizer': model_tokenizer}).
                     These are merged with the rule's static parameters definition.

        Returns:
            The result of the rule function (bool, string, list, or dict).
        """
        if rule_id not in self.metadata:
            raise ValueError(f"Rule ID '{rule_id}' not found in metadata.")

        rule_info = self.metadata[rule_id]
        func_name = rule_info['function']
        static_params = rule_info.get('params', {})

        func = self._get_function(func_name)

        # Merge static parameters with runtime context
        # Runtime context wins if there's a collision (allows overriding defaults)
        kwargs = static_params.copy()
        if context:
            kwargs.update(context)

        # Filter arguments to match the function signature
        # This prevents passing unused arguments to functions that don't accept **kwargs
        sig = inspect.signature(func)
        valid_params = {}

        # The first parameter is positional (input_data), so we skip it in kwargs matching
        params_iterator = iter(sig.parameters.items())
        try:
            next(params_iterator) # Skip first param (text/input)
        except StopIteration:
            pass 

        for name, param in params_iterator:
            if name in kwargs:
                valid_params[name] = kwargs[name]
            elif param.default == inspect.Parameter.empty:
                # If a required param is missing from kwargs, we assume the user 
                # might have intended to pass it, or it will raise TypeError at call time.
                pass

        return func(input_data, **valid_params)

    def process_pipeline(self, input_data: Any, rule_ids: List[str], context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Runs a sequence of transformation rules.
        
        If an intermediate result is a list (e.g. from sentence splitting or chunking),
        subsequent rules are applied to each element of the list.

        Args:
            input_data: Initial text or data.
            rule_ids: List of rule IDs to execute in order.
            context: Runtime context arguments.

        Returns:
            The final processed data (str or list of str).
        """
        current_data = input_data

        for rule_id in rule_ids:
            # Determine if we need to map over a list
            if isinstance(current_data, list):
                # Apply rule to each item in the list
                current_data = [
                    self.apply_rule(rule_id, item, context) 
                    for item in current_data
                ]
            else:
                # Apply rule to the single item
                current_data = self.apply_rule(rule_id, current_data, context)

        return current_data

    def validate_all(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        Runs all confirmation/validation rules (Category: 'validation') against the text.

        Returns:
            Dict mapping rule_id to boolean result.
        """
        results = {}
        for rule_id, rule_def in self.metadata.items():
            if rule_def.get('category') == 'validation':
                results[rule_id] = self.apply_rule(rule_id, text, context)
        return results

    def get_rule_info(self, rule_id: str) -> Dict[str, Any]:
        """Returns metadata for a specific rule."""
        return self.metadata.get(rule_id, {})
