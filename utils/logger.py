# -*- coding: utf-8 -*-
"""
Centralized logging for the Select Matching Features plugin.
Standardizes all QgsMessageLog calls throughout the codebase.
"""

from qgis.core import QgsMessageLog, Qgis


class PluginLogger:
    """
    Centralized logging for the plugin.
    
    Usage:
        PluginLogger.info("Tool activated")
        PluginLogger.warning("No features selected")
        PluginLogger.error("Failed to apply filter")
    """
    
    PLUGIN_NAME = 'Select Matching Features'
    
    @classmethod
    def info(cls, message):
        """
        Log info message.
        
        Args:
            message: Message to log
        """
        QgsMessageLog.logMessage(message, cls.PLUGIN_NAME, Qgis.Info)
    
    @classmethod
    def warning(cls, message):
        """
        Log warning message.
        
        Args:
            message: Message to log
        """
        QgsMessageLog.logMessage(message, cls.PLUGIN_NAME, Qgis.Warning)
    
    @classmethod
    def error(cls, message):
        """
        Log error message.
        
        Args:
            message: Message to log
        """
        QgsMessageLog.logMessage(message, cls.PLUGIN_NAME, Qgis.Critical)
    
    @classmethod
    def debug(cls, message):
        """
        Log debug message (only if debug is enabled).
        
        Args:
            message: Message to log
        """
        # Could be controlled by settings in the future
        QgsMessageLog.logMessage(f"DEBUG: {message}", cls.PLUGIN_NAME, Qgis.Info)
