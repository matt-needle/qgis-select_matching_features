# -*- coding: utf-8 -*-
from qgis.gui import QgsHighlight
from qgis.PyQt.QtGui import QColor


class HighlightManager:
    """
    Manages feature highlights on the map canvas.
    
    Usage:
        highlight_mgr = HighlightManager(canvas)
        highlight_mgr.add_highlight('reference', geometry, layer)
        highlight_mgr.remove_highlight('reference')
    """
    
    def __init__(self, canvas):
        """
        Initialize the highlight manager.
        
        Args:
            canvas: QgsMapCanvas instance
        """
        self.canvas = canvas
        self.highlights = {}
    
    def add_highlight(self, name, geometry, layer, color=None, width=2):
        """
        Add or update a named highlight.
        
        Args:
            name: Unique identifier for this highlight
            geometry: Feature geometry to highlight
            layer: Vector layer the feature belongs to
            color: Optional QColor for the highlight (default: orange)
            width: Line width for the highlight (default: 2)
        """
        # Remove old highlight if exists
        self.remove_highlight(name)
        
        # Create new highlight
        highlight = QgsHighlight(self.canvas, geometry, layer)
        
        # Set colors
        if color is None:
            color = QColor(255, 50, 0)  # Default orange
        
        highlight.setColor(color)
        highlight.setFillColor(QColor(0, 0, 0, 0))  # Transparent fill
        highlight.setWidth(width)
        highlight.show()
        
        self.highlights[name] = highlight
    
    def remove_highlight(self, name):
        """
        Remove a named highlight.
        
        Args:
            name: Identifier of the highlight to remove
            
        Returns:
            bool: True if highlight was removed, False if didn't exist
        """
        if name in self.highlights:
            self.highlights[name].hide()
            del self.highlights[name]
            return True
        return False
    
    def has_highlight(self, name):
        """
        Check if a named highlight exists.
        
        Args:
            name: Identifier of the highlight
            
        Returns:
            bool: True if highlight exists
        """
        return name in self.highlights
    
    def clear_all(self):
        """Remove all highlights."""
        for highlight in self.highlights.values():
            highlight.hide()
        self.highlights.clear()
    
    def get_highlight_names(self):
        """
        Get list of all highlight names.
        
        Returns:
            list: List of highlight identifiers
        """
        return list(self.highlights.keys())
