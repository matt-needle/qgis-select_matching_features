# -*- coding: utf-8 -*-
class OperatorManager:
    """
    Manages comparison operators and their properties.
    
    Usage:
        if OperatorManager.is_null_compatible(operator):
            expr = OperatorManager.get_null_expression(operator, field_name)
    """
    
    # Operator definitions with properties
    OPERATORS = {
        '=': {
            'symbol': '=',
            'name': 'Equal',
            'sql_null': 'IS NULL'
        },
        '!=': {
            'symbol': '!=',
            'name': 'Not Equal',
            'sql_null': 'IS NOT NULL'
        },
        '<': {
            'symbol': '<',
            'name': 'Less Than',
            'sql_null': None
        },
        '>': {
            'symbol': '>',
            'name': 'Greater Than',
            'sql_null': None
        },
        '<=': {
            'symbol': '<=',
            'name': 'Less or Equal',
            'sql_null': None
        },
        '>=': {
            'symbol': '>=',
            'name': 'Greater or Equal',
            'sql_null': None
        }
    }
    
    @classmethod
    def is_null_compatible(cls, operator):
        """
        Check if operator can work with NULL values.
        
        Args:
            operator: Operator symbol
            
        Returns:
            bool: True if operator can handle NULL
        """
        return cls.OPERATORS.get(operator, {}).get('sql_null') is not None
    
    @classmethod
    def get_null_sql(cls, operator):
        """
        Get SQL expression for NULL comparison.
        
        Args:
            operator: Operator symbol
            
        Returns:
            str: SQL NULL expression or None if not compatible
        """
        return cls.OPERATORS.get(operator, {}).get('sql_null')
    
    @classmethod
    def validate_operator(cls, operator):
        """
        Check if operator is valid.
        
        Args:
            operator: Operator symbol to validate
            
        Returns:
            bool: True if operator is valid
        """
        return operator in cls.OPERATORS
    
    @classmethod
    def get_operator_name(cls, operator):
        """
        Get human-readable name for operator.
        
        Args:
            operator: Operator symbol
            
        Returns:
            str: Operator name
        """
        return cls.OPERATORS.get(operator, {}).get('name', operator)
