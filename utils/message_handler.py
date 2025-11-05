# -*- coding: utf-8 -*-
from qgis.core import Qgis

class MessageHandler:
    """
    Handles all user-facing messages in the QGIS interface.
    
    Usage:
        handler = MessageHandler(iface)
        handler.show_success("Operation completed successfully")
        handler.show_warning("Please select a layer")
        handler.show_error("An error occurred")
    """
    
    def __init__(self, iface):
        """
        Initialize the message handler.
        
        Args:
            iface: QGIS interface object
        """
        self.iface = iface
    
    def show_success(self, message, title="Success", duration=0):
        """
        Display a success message (green bar).
        
        Args:
            message: Message text to display
            title: Message title (default: "Success")
            duration: How long to show message in seconds (0 = until dismissed)
        """
        self._show_message(title, message, Qgis.Success, duration)
    
    def show_warning(self, message, title="Warning", duration=0):
        """
        Display a warning message (yellow/orange bar).
        
        Args:
            message: Message text to display
            title: Message title (default: "Warning")
            duration: How long to show message in seconds (0 = until dismissed)
        """
        self._show_message(title, message, Qgis.Warning, duration)
    
    def show_error(self, message, title="Error", duration=0):
        """
        Display an error message (red bar).
        
        Args:
            message: Message text to display
            title: Message title (default: "Error")
            duration: How long to show message in seconds (0 = until dismissed)
        """
        self._show_message(title, message, Qgis.Critical, duration)
    
    def show_info(self, message, title="Info", duration=3):
        """
        Display an info message (blue bar).
        
        Args:
            message: Message text to display
            title: Message title (default: "Info")
            duration: How long to show message in seconds (default: 3)
        """
        self._show_message(title, message, Qgis.Info, duration)
    
    def _show_message(self, title, message, level, duration):
        """
        Internal method to handle all message types.
        Automatically clears previous messages before showing new one.
        
        Args:
            title: Message title
            message: Message text
            level: Qgis message level (Success, Warning, Critical, Info)
            duration: Display duration in seconds
        """
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            title,
            message,
            level=level,
            duration=duration
        )
    
    def clear(self):
        """Clear all messages from the message bar."""
        self.iface.messageBar().clearWidgets()
