# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QSettings


class SettingsManager:
    """
    Manages all plugin settings with a single source of truth for setting keys.
    
    Usage:
        settings = SettingsManager()
        layer_id = settings.get_current_layer()
        settings.set_current_layer('layer_123')
    """
    
    # Settings keys as class constants - single source of truth
    KEY_CURRENT_LAYER = '/SelectMatchingFeatures/currentLayer'
    KEY_CURRENT_FIELD = '/SelectMatchingFeatures/currentField'
    KEY_HIDE_NON_MATCHING = '/SelectMatchingFeatures/hideNonMatching'
    KEY_SELECT_FILTERED = '/SelectMatchingFeatures/selectFiltered'
    KEY_OPERATOR = '/SelectMatchingFeatures/operator'
    KEY_ADVANCED_COLLAPSED = '/SelectMatchingFeatures/advancedCollapsed'
    
    def __init__(self):
        """Initialize the settings manager."""
        self.settings = QSettings()
    
    # Layer settings
    def get_current_layer(self):
        """
        Get the saved layer ID.
        
        Returns:
            str: Layer ID or empty string if not set
        """
        return self.settings.value(self.KEY_CURRENT_LAYER, '')
    
    def set_current_layer(self, layer_id):
        """
        Save the current layer ID.
        
        Args:
            layer_id: QGIS layer ID string
        """
        if layer_id:
            self.settings.setValue(self.KEY_CURRENT_LAYER, layer_id)
    
    # Field settings
    def get_current_field(self):
        """
        Get the saved field name.
        
        Returns:
            str: Field name or empty string if not set
        """
        return self.settings.value(self.KEY_CURRENT_FIELD, '')
    
    def set_current_field(self, field_name):
        """
        Save the current field name.
        
        Args:
            field_name: Name of the field
        """
        if field_name:
            self.settings.setValue(self.KEY_CURRENT_FIELD, field_name)
    
    # Mode settings
    def get_hide_non_matching(self):
        """
        Get the selection mode (hide vs select).
        
        Returns:
            bool: True if hide mode, False if select mode
        """
        return self.settings.value(self.KEY_HIDE_NON_MATCHING, False, type=bool)
    
    def set_hide_non_matching(self, hide_mode):
        """
        Save the selection mode.
        
        Args:
            hide_mode: True for hide mode, False for select mode
        """
        self.settings.setValue(self.KEY_HIDE_NON_MATCHING, hide_mode)
    
    # Select filtered settings
    def get_select_filtered(self):
        """
        Get the "select filtered" checkbox state.
        
        Returns:
            bool: True if checkbox should be checked
        """
        return self.settings.value(self.KEY_SELECT_FILTERED, False, type=bool)
    
    def set_select_filtered(self, select_filtered):
        """
        Save the "select filtered" checkbox state.
        
        Args:
            select_filtered: True if checkbox is checked
        """
        self.settings.setValue(self.KEY_SELECT_FILTERED, select_filtered)
    
    # Operator settings
    def get_operator(self):
        """
        Get the saved comparison operator.
        
        Returns:
            str: Operator symbol ('=', '!=', '<', '>', '<=', '>=')
        """
        return self.settings.value(self.KEY_OPERATOR, '=')
    
    def set_operator(self, operator):
        """
        Save the comparison operator.
        
        Args:
            operator: Operator symbol ('=', '!=', '<', '>', '<=', '>=')
        """
        if operator in ['=', '!=', '<', '>', '<=', '>=']:
            self.settings.setValue(self.KEY_OPERATOR, operator)
    
    # Advanced section settings
    def get_advanced_collapsed(self):
        """
        Get whether the advanced section should be collapsed.
        
        Returns:
            bool: True if collapsed, False if expanded
        """
        return self.settings.value(self.KEY_ADVANCED_COLLAPSED, True, type=bool)
    
    def set_advanced_collapsed(self, collapsed):
        """
        Save the advanced section collapsed state.
        
        Args:
            collapsed: True if collapsed, False if expanded
        """
        self.settings.setValue(self.KEY_ADVANCED_COLLAPSED, collapsed)
    
    def reset_all(self):
        """Reset all plugin settings to defaults."""
        for key in [self.KEY_CURRENT_LAYER, self.KEY_CURRENT_FIELD, 
                    self.KEY_HIDE_NON_MATCHING, self.KEY_SELECT_FILTERED,
                    self.KEY_OPERATOR, self.KEY_ADVANCED_COLLAPSED]:
            self.settings.remove(key)
