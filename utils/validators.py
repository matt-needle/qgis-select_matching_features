# -*- coding: utf-8 -*-
class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validator:
    """
    Validates plugin inputs with consistent error messages.
    
    Usage:
        try:
            Validator.validate_layer(layer)
            Validator.validate_field(field_name)
            # ... proceed with operation
        except ValidationError as e:
            message_handler.show_warning(str(e))
    """
    
    @staticmethod
    def validate_layer(layer):
        """
        Validate that a layer exists and is valid.
        
        Args:
            layer: QgsVectorLayer to validate
            
        Raises:
            ValidationError: If layer is None or invalid
            
        Returns:
            bool: True if valid
        """
        if not layer:
            raise ValidationError("Please select a layer")
        
        if not layer.isValid():
            raise ValidationError(f"Layer '{layer.name()}' is not valid")
        
        return True
    
    @staticmethod
    def validate_field(field_name, layer=None):
        """
        Validate that a field name exists.
        
        Args:
            field_name: Name of the field to validate
            layer: Optional layer to check if field exists in layer
            
        Raises:
            ValidationError: If field_name is empty or doesn't exist in layer
            
        Returns:
            bool: True if valid
        """
        if not field_name:
            raise ValidationError("Please select a field")
        
        # If layer provided, check if field exists in layer
        if layer:
            field_names = [field.name() for field in layer.fields()]
            if field_name not in field_names:
                raise ValidationError(
                    f"Field '{field_name}' does not exist in layer '{layer.name()}'"
                )
        
        return True
    
    @staticmethod
    def validate_layer_and_field(layer, field_name):
        """
        Validate both layer and field in one call.
        
        Args:
            layer: QgsVectorLayer to validate
            field_name: Field name to validate
            
        Raises:
            ValidationError: If either validation fails
            
        Returns:
            bool: True if both are valid
        """
        Validator.validate_layer(layer)
        Validator.validate_field(field_name, layer)
        return True
    
    @staticmethod
    def validate_primary_key(layer):
        """
        Validate that a layer has a primary key defined.
        
        Args:
            layer: QgsVectorLayer to validate
            
        Raises:
            ValidationError: If layer has no primary key
            
        Returns:
            bool: True if layer has primary key
        """
        Validator.validate_layer(layer)
        
        pk_indexes = layer.primaryKeyAttributes()
        if not pk_indexes:
            raise ValidationError(
                f"Layer '{layer.name()}' has no primary key. "
                "Cannot apply filter without a primary key."
            )
        
        return True
    
    @staticmethod
    def validate_selection_exists(layer):
        """
        Validate that a layer has selected features.
        
        Args:
            layer: QgsVectorLayer to validate
            
        Raises:
            ValidationError: If no features are selected
            
        Returns:
            int: Number of selected features
        """
        Validator.validate_layer(layer)
        
        count = layer.selectedFeatureCount()
        if count == 0:
            raise ValidationError("No features are selected")
        
        return count
