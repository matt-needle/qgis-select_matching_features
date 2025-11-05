# -*- coding: utf-8 -*-
from ..utils.operators import OperatorManager


class ExpressionBuilder:
    """
    Builds QGIS selection expressions for different data types and operators.
    
    Usage:
        expr, display = ExpressionBuilder.build_expression("field_name", "=", "value")
        layer.selectByExpression(expr)
        print(f"Selected where field_name = {display}")
    """
    
    @staticmethod
    def build_expression(field_name, operator, value):
        """
        Build a QGIS expression string for feature selection.
        
        Args:
            field_name: Name of the field to query
            operator: Comparison operator (=, !=, <, >, <=, >=)
            value: Value to compare against (can be None for NULL)
            
        Returns:
            tuple: (expression_string, display_value_string)
                - expression_string: QGIS expression for selectByExpression()
                - display_value_string: Human-readable value for UI display
                
        Raises:
            ValueError: If operator cannot be used with NULL values
        """
        if value is None:
            return ExpressionBuilder._build_null_expression(field_name, operator)
        elif isinstance(value, str):
            return ExpressionBuilder._build_string_expression(field_name, operator, value)
        else:
            return ExpressionBuilder._build_numeric_expression(field_name, operator, value)
    
    @staticmethod
    def _build_null_expression(field_name, operator):
        """
        Build expression for NULL value comparisons.
        
        Args:
            field_name: Name of the field
            operator: Comparison operator (only = and != are valid)
            
        Returns:
            tuple: (expression, display_value)
            
        Raises:
            ValueError: If operator is not = or !=
        """
        if not OperatorManager.is_null_compatible(operator):
            raise ValueError(
                f"Operator '{operator}' cannot be used with NULL values. "
                f"Only '=' (IS NULL) and '!=' (IS NOT NULL) are supported."
            )
        
        null_sql = OperatorManager.get_null_sql(operator)
        expr = f'"{field_name}" {null_sql}'
        return expr, "NULL"
    
    @staticmethod
    def _build_string_expression(field_name, operator, value):
        """
        Build expression for string value comparisons.
        Properly escapes single quotes in the value.
        
        Args:
            field_name: Name of the field
            operator: Comparison operator
            value: String value to compare
            
        Returns:
            tuple: (expression, display_value)
        """
        # Escape single quotes by doubling them (SQL standard)
        escaped_value = value.replace("'", "''")
        expr = f'"{field_name}" {operator} \'{escaped_value}\''
        display_value = f"'{value}'"
        return expr, display_value
    
    @staticmethod
    def _build_numeric_expression(field_name, operator, value):
        """
        Build expression for numeric value comparisons.
        
        Args:
            field_name: Name of the field
            operator: Comparison operator
            value: Numeric value to compare
            
        Returns:
            tuple: (expression, display_value)
        """
        expr = f'"{field_name}" {operator} {value}'
        display_value = str(value)
        return expr, display_value
