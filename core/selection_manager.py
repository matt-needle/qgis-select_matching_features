# -*- coding: utf-8 -*-
from ..utils.logger import PluginLogger


class SelectionManager:
    """
    Handles all selection and filtering operations on layers.
    
    IMPORTANT: This class fixes the critical bug where internal QGIS feature IDs
    were being used instead of actual primary key field values.
    
    Usage:
        success, count, error = SelectionManager.apply_filter_to_selection(layer)
        if success:
            print(f"Filtered to {count} features")
        else:
            print(f"Error: {error}")
    """
    
    @staticmethod
    def apply_filter_to_selection(layer):
        """
        Apply a subset string filter to show only currently selected features.
        Uses the layer's primary key FIELD VALUES (not internal feature IDs).
        
        Args:
            layer: QgsVectorLayer to filter
            
        Returns:
            tuple: (success: bool, count: int, error_message: str)
                - success: True if filter was applied successfully
                - count: Number of features in the filter
                - error_message: Error description if success is False, empty otherwise
        """
        if not layer:
            return False, 0, "No layer provided"
        
        if SelectionManager.has_edit_session(layer):
            return False, 0, "Filter cannot be applied: Layer has an active edit session"
        
        selected_features = layer.selectedFeatures()
        if not selected_features:
            return False, 0, "No features selected"
        
        # Check for primary key
        pk_indexes = layer.primaryKeyAttributes()
        if not pk_indexes:
            return False, 0, "Layer has no primary key"
        
        try:
            # Get the primary key field name
            pk_field_name = layer.fields()[pk_indexes[0]].name()
            
            # BUG FIX: Extract ACTUAL primary key field values from features
            # (not internal QGIS feature IDs)
            pk_values = []
            for feature in selected_features:
                pk_value = feature[pk_field_name]
                
                # Handle NULL values
                if pk_value is None or (hasattr(pk_value, 'isNull') and pk_value.isNull()):
                    continue
                    
                pk_values.append(pk_value)
            
            if not pk_values:
                return False, 0, "No valid primary key values found in selected features"
            
            # Determine if values are strings (need quoting) or numeric
            first_value = pk_values[0]
            if isinstance(first_value, str):
                # String values need to be quoted and escaped
                escaped_values = [value.replace("'", "''") for value in pk_values]
                value_list = ','.join([f"'{value}'" for value in escaped_values])
            else:
                # Numeric values don't need quoting
                value_list = ','.join(map(str, pk_values))
            
            # Build and apply the filter
            filter_string = f'"{pk_field_name}" IN ({value_list})'
            layer.setSubsetString(filter_string)
            
            PluginLogger.info(
                f"Applied filter to {len(pk_values)} features: {filter_string[:100]}"
            )
            
            return True, len(pk_values), ""
            
        except IndexError as e:
            error_msg = f"Primary key field not found: {str(e)}"
            PluginLogger.error(error_msg)
            return False, 0, error_msg
        except Exception as e:
            error_msg = f"Failed to apply filter: {str(e)}"
            PluginLogger.error(error_msg)
            return False, 0, error_msg
    
    @staticmethod
    def clear_filter(layer):
        """
        Remove any active subset string filter from the layer.
        
        Args:
            layer: QgsVectorLayer to clear filter from
            
        Returns:
            bool: True if filter was cleared (or no filter existed), False on error
        """
        if not layer:
            return False
        
        try:
            layer.setSubsetString('')
            PluginLogger.info(f"Cleared filter from layer: {layer.name()}")
            return True
        except Exception as e:
            PluginLogger.error(f"Error clearing filter: {str(e)}")
            return False
    
    @staticmethod
    def clear_selection(layer):
        """
        Clear the selection on the layer.
        
        Args:
            layer: QgsVectorLayer to clear selection from
            
        Returns:
            bool: True if selection was cleared, False on error
        """
        if not layer:
            return False
        
        try:
            layer.removeSelection()
            return True
        except Exception as e:
            PluginLogger.error(f"Error clearing selection: {str(e)}")
            return False
    
    @staticmethod
    def select_all_in_filter(layer):
        """
        Select all features currently visible after a filter is applied.
        
        Args:
            layer: QgsVectorLayer to select from
            
        Returns:
            int: Number of features selected, -1 on error
        """
        if not layer:
            return -1
        
        try:
            layer.selectAll()
            count = layer.selectedFeatureCount()
            PluginLogger.info(f"Selected {count} filtered features")
            return count
        except Exception as e:
            PluginLogger.error(f"Error selecting filtered features: {str(e)}")
            return -1
        
    @staticmethod
    def has_edit_session(layer):
        """
        Check if layer has no active edit session

        Args: 
            layer QgsVectorLayer to check
        
        Returns:
            bool: True if no edit session is active, False otherwise
        """
        return layer.isEditable()
        
    
    @staticmethod
    def has_active_filter(layer):
        """
        Check if the layer has an active subset string filter.
        
        Args:
            layer: QgsVectorLayer to check
            
        Returns:
            bool: True if filter is active, False otherwise
        """
        if not layer:
            return False
        return bool(layer.subsetString())
    
    @staticmethod
    def get_filtered_feature_ids(layer):
        """
        Get the feature IDs of currently visible (filtered) features.
        Call this BEFORE clearing the filter to get the IDs to select.
        
        Args:
            layer: QgsVectorLayer with active filter
            
        Returns:
            list: List of feature IDs currently visible, empty list if no filter or error
        """
        if not layer or not layer.subsetString():
            return []
        
        try:
            # Get all currently visible features (after filter is applied)
            feature_ids = []
            for feature in layer.getFeatures():
                feature_ids.append(feature.id())
            
            PluginLogger.info(f"Retrieved {len(feature_ids)} filtered feature IDs")
            return feature_ids
        except Exception as e:
            PluginLogger.error(f"Error getting filtered feature IDs: {str(e)}")
            return []
    
    @staticmethod
    def clear_filter_and_select_features(layer):
        """
        Clear the filter and select the features that were previously filtered.
        This is useful when switching from filter mode to select mode.
        
        Args:
            layer: QgsVectorLayer with active filter
            
        Returns:
            tuple: (success: bool, count: int, error_message: str)
        """
        if not layer:
            return False, 0, "No layer provided"
        
        if not layer.subsetString():
            return False, 0, "No active filter to clear"
        
        try:
            # Get IDs of currently filtered features BEFORE clearing filter
            filtered_ids = SelectionManager.get_filtered_feature_ids(layer)
            
            if not filtered_ids:
                return False, 0, "No features in filter"
            
            # Clear the filter
            layer.setSubsetString('')
            
            # Select the features that were filtered
            layer.selectByIds(filtered_ids)
            
            count = len(filtered_ids)
            PluginLogger.info(f"Cleared filter and selected {count} features")
            
            return True, count, ""
            
        except Exception as e:
            error_msg = f"Failed to clear filter and select features: {str(e)}"
            PluginLogger.error(error_msg)
            return False, 0, error_msg
