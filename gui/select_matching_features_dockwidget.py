# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectMatchingFeaturesDockWidget
                                 A QGIS plugin
 Clicking a feature will select all features in layer with same attribute value
                             -------------------
        begin                : 2022-01-29
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Matt
        email                : m_needle@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), '..', 'select_matching_features_dockwidget_base.ui'))


class SelectMatchingFeaturesDockWidget(QDockWidget, FORM_CLASS):
    """
    Docked widget for configuring and activating the Select Matching Features tool.
    Refactored to use SettingsManager instead of direct QSettings access.
    """
    
    # Signals
    toolActivated = pyqtSignal(bool)
    showAllFeaturesRequested = pyqtSignal()
    selectFilteredChanged = pyqtSignal(bool)
    applyFilterToSelection = pyqtSignal()
    clearFilterAndSelectFiltered = pyqtSignal()
    
    def __init__(self, iface, settings_manager, parent=None):
        """
        Constructor.
        
        Args:
            iface: QGIS interface
            settings_manager: SettingsManager instance for loading/saving settings
            parent: Parent widget
        """
        super(SelectMatchingFeaturesDockWidget, self).__init__(parent)
        self.iface = iface
        self.settings_manager = settings_manager
        self.setupUi(self)
        
        # Connect UI signals
        self._connect_signals()
        
        # Initialize combos and load settings
        self.setup_combos()
        self.load_settings()
        
    def _connect_signals(self):
        """Connect all UI signals to their handlers."""
        # Button signals
        self.btnActivateTool.clicked.connect(self.on_activate_tool_clicked)
        self.btnShowAllFeatures.clicked.connect(self.on_show_all_features_clicked)
        
        # Checkbox signals
        self.chkSelectFiltered.toggled.connect(self.on_select_filtered_toggled)
        
        # Radio button signals (operators)
        self.radioOpEqual.toggled.connect(self.on_operator_changed)
        self.radioOpNotEqual.toggled.connect(self.on_operator_changed)
        self.radioOpLessThan.toggled.connect(self.on_operator_changed)
        self.radioOpGreaterThan.toggled.connect(self.on_operator_changed)
        self.radioOpLessEqual.toggled.connect(self.on_operator_changed)
        self.radioOpGreaterEqual.toggled.connect(self.on_operator_changed)
        
        # Radio button signals (mode)
        self.radioSelectMatching.toggled.connect(self.on_mode_changed)
        self.radioHideNonMatching.toggled.connect(self.on_mode_changed)
        
        # Advanced section
        self.grpAdvanced.collapsedStateChanged.connect(self.on_advanced_collapsed)
        
    def setup_combos(self):
        """Initialize the layer and field combo boxes"""
        project = QgsProject.instance()
        layers = project.mapLayers()
        
        if layers:
            # Set the active layer as default
            current_layer = self.iface.activeLayer()
            
            if current_layer:
                self.mLayerCombo.setAllowEmptyLayer(False)
                self.mLayerCombo.setLayer(current_layer)
            elif layers:
                self.mLayerCombo.setAllowEmptyLayer(False)
                self.mLayerCombo.setCurrentIndex(0)
            else:
                self.mLayerCombo.setAllowEmptyLayer(True)
                
        # Connect layer combo to field combo
        if layers:
            self.mFieldCombo.setLayer(self.mLayerCombo.currentLayer())
            self.mLayerCombo.layerChanged.connect(
                lambda: self.mFieldCombo.setLayer(self.mLayerCombo.currentLayer())
            )
            
            # Connect to save settings when layer or field changes
            self.mLayerCombo.layerChanged.connect(self.save_settings)
            self.mFieldCombo.fieldChanged.connect(self.save_settings)

    def on_mode_changed(self):
        """Handle when selection mode changes"""
        layer = self.get_current_layer()

        # Check if we're switching TO filter mode FROM select mode
        if self.radioHideNonMatching.isChecked() and layer:
            if layer.selectedFeatureCount() > 0:
                # Emit signal to main plugin to apply filter to current selection
                self.applyFilterToSelection.emit()
        
        # Check if we're switching TO select mode FROM filter mode
        elif self.radioSelectMatching.isChecked() and layer:
            if layer.subsetString():
                # There's an active filter - emit signal to clear it and select filtered features
                self.clearFilterAndSelectFiltered.emit()

        self.save_settings()
        self.update_button_text()

        # Update button enabled state based on current layer state
        if layer:
            if self.radioHideNonMatching.isChecked():
                # Hide mode: Enable if filter is active OR if there's a selection
                if layer.subsetString() or layer.selectedFeatureCount() > 0:
                    self.enable_show_all_button(True)
                else:
                    self.enable_show_all_button(False)
            else:
                # Select mode: Always keep button enabled
                self.enable_show_all_button(True)

    def load_settings(self):
        """Load saved settings using SettingsManager"""
        # Load layer
        layer_id = self.settings_manager.get_current_layer()
        if layer_id:
            layer = QgsProject.instance().mapLayer(layer_id)
            if layer:
                self.mLayerCombo.setLayer(layer)
                self.mFieldCombo.setLayer(layer)

        # Load field
        field_name = self.settings_manager.get_current_field()
        if field_name:
            self.mFieldCombo.setField(field_name)

        # Load selection mode
        hide_mode = self.settings_manager.get_hide_non_matching()
        if hide_mode:
            self.radioHideNonMatching.setChecked(True)
        else:
            self.radioSelectMatching.setChecked(True)

        # Load select filtered checkbox state
        select_filtered = self.settings_manager.get_select_filtered()
        self.chkSelectFiltered.setChecked(select_filtered)

        # Load operator
        operator = self.settings_manager.get_operator()
        self._set_operator_radio(operator)

        # Update button text based on loaded mode
        self.update_button_text()

    def _set_operator_radio(self, operator):
        """
        Set the appropriate operator radio button.
        
        Args:
            operator: Operator symbol ('=', '!=', '<', '>', '<=', '>=')
        """
        operator_radios = {
            '=': self.radioOpEqual,
            '!=': self.radioOpNotEqual,
            '<': self.radioOpLessThan,
            '>': self.radioOpGreaterThan,
            '<=': self.radioOpLessEqual,
            '>=': self.radioOpGreaterEqual
        }
        
        radio = operator_radios.get(operator, self.radioOpEqual)
        radio.setChecked(True)

    def save_settings(self):
        """Save current settings using SettingsManager"""
        # Save layer
        current_layer = self.mLayerCombo.currentLayer()
        if current_layer:
            self.settings_manager.set_current_layer(current_layer.id())

        # Save field
        current_field = self.mFieldCombo.currentField()
        if current_field:
            self.settings_manager.set_current_field(current_field)

        # Save selection mode
        self.settings_manager.set_hide_non_matching(self.radioHideNonMatching.isChecked())

        # Save select filtered checkbox state
        self.settings_manager.set_select_filtered(self.chkSelectFiltered.isChecked())

        # Save operator
        self.settings_manager.set_operator(self.get_operator())
    
    def on_activate_tool_clicked(self, checked):
        """Handle the activate tool button click"""
        self.toolActivated.emit(checked)
        
        # Update button text based on state
        if checked:
            self.btnActivateTool.setText("Deactivate Selection Tool")
        else:
            self.btnActivateTool.setText("Activate Selection Tool")
    
    def on_show_all_features_clicked(self):
        """Handle the show all features button click"""
        self.showAllFeaturesRequested.emit()
    
    def update_button_text(self):
        """Update the button text based on the current selection mode"""
        if self.radioHideNonMatching.isChecked():
            self.btnShowAllFeatures.setText("Show All Features")
            self.btnShowAllFeatures.setToolTip("Clear filter and show all features in the layer")
        else:
            self.btnShowAllFeatures.setText("Clear Selection")
            self.btnShowAllFeatures.setToolTip("Clear the current selection")
    
    def enable_show_all_button(self, enabled):
        """Enable or disable the show all features button"""
        self.btnShowAllFeatures.setEnabled(enabled)
        self.update_button_text()
    
    def get_current_layer(self):
        """Return the currently selected layer"""
        return self.mLayerCombo.currentLayer()
    
    def get_current_field(self):
        """Return the currently selected field"""
        return self.mFieldCombo.currentField()
    
    def get_selection_mode(self):
        """Return the selection mode (True = hide non-matching, False = select only)"""
        return self.radioHideNonMatching.isChecked()
    
    def set_tool_active(self, active):
        """Set the tool button state without triggering the clicked signal"""
        self.btnActivateTool.blockSignals(True)
        self.btnActivateTool.setChecked(active)
        if active:
            self.btnActivateTool.setText("Deactivate Selection Tool")
        else:
            self.btnActivateTool.setText("Activate Selection Tool")
        self.btnActivateTool.blockSignals(False)

    def on_select_filtered_toggled(self, checked):
        """Handle when select filtered checkbox is toggled"""
        self.selectFilteredChanged.emit(checked)

    def get_select_filtered_state(self):
        """Return whether select filtered checkbox is checked"""
        return self.chkSelectFiltered.isChecked()

    def on_operator_changed(self):
        """Handle when operator selection changes"""
        self.save_settings()

    def get_operator(self):
        """Return the currently selected operator (always = when Advanced is collapsed)"""
        # If Advanced section is collapsed, always use = operator
        if self.grpAdvanced.isCollapsed():
            return "="

        # Otherwise return the selected operator
        if self.radioOpEqual.isChecked():
            return "="
        elif self.radioOpNotEqual.isChecked():
            return "!="
        elif self.radioOpLessThan.isChecked():
            return "<"
        elif self.radioOpGreaterThan.isChecked():
            return ">"
        elif self.radioOpLessEqual.isChecked():
            return "<="
        elif self.radioOpGreaterEqual.isChecked():
            return ">="
        else:
            return "="  # Default

    def on_advanced_collapsed(self, collapsed):
        """Handle when Advanced section is collapsed/expanded"""
        if collapsed:
            # When collapsed, revert to = operator
            self.radioOpEqual.setChecked(True)
            self.save_settings()
