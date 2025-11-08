# Select Matching Features
![select_matching_features_demo](https://github.com/user-attachments/assets/eaf2d69e-e626-4d8a-97be-dce1b2df036a)

### How to use
- Find the tool in the Selection toolbar  
  <img width="275" height="68" alt="image" src="https://github.com/user-attachments/assets/98de45a5-5564-402b-ab58-709b7114972f" />
- A pane will appear in the bottom right of the QGIS window (the can be re-docked in a different place)
- Select the layer and the field to match using the menus
- Click <kbd>Activate Selection Tool</kbd>
- Click a feature on the map to select all features with a matching attribute value
- See the message bar for the number of selected features and the matching attribute value
- Choose between selecting and filtering the matching features (the reference feature is outlined in red)
- Click empty space to clear the selection (or use the <kbd>Clear Selection</kbd> / <kbd>Show all features</kbd> button)
- Expand the Advanced section to use common operators such as Less Than or Equal to, Greater Than, etc

### Known issues
- There is a bug where if the tool is active and another map tool is activated (Pan, Identify, etc) the Select Matching Features tool does not automatically deactivate
  - To reactivate the tool in this case, the <kbd>Deactivate Selection Tool</kbd> button must be clicked followed by the <kbd>Activate Selection Tool</kbd> button
  - This bug will be addressed in the next version
- If the target layer has an active edit session filtering will not be applied. This is normal QGIS behaviour but there is no indication from the tool why the filter failed.
  - This will be addressed in the next version with a message to indicate why the filter has not beein applied  
