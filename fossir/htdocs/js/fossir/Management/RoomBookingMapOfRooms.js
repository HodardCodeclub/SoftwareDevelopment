
function aspectListNothing(data, func) {
    each(data, function() {
        func(true);
    });
}

function singleAspectNothing(user, func) {
    func(true);
}

/**
 * Creates an aspect creation / edit pop-up dialog.
 * @param {String} title The title of the popup.
 * @param {Object} aspectData A WatchObject that has to have the following keys/attributes:
 *                          id, name, centerLatitude, centerLongitude, topLeftLatitude, topLeftLongitude,
 *                          bottomRightLatitude, bottomRightLongitude, zoomLevel, defaultOnStartup.
 *                          Its information will be displayed as initial values in the dialog.
 * @param {Function} action A callback function that will be called if the aspect presses ok.
 *                          The function will be passed a WatchObject with the new values.
 */
type("MapAspectDataPopup", ["ExclusivePopupWithButtons"],
    {
        param: function(aspectData, label, propertyName) {
            var edit = Html.edit({style: {width: '300px'}});
            var accessor = aspectData.accessor(propertyName);
            this.parameterManager.add(edit, 'text', false);
            var binding = $B(edit, accessor);
            return [$T(label), binding];
        },

        draw: function() {
            var aspectData = this.aspectData;
            var self = this;
            self.parameterManager = new fossirUtil.parameterManager();

            var form = fossirUtil.createFormFromMap([
                this.param(aspectData, 'Name', 'name'),
                this.param(aspectData, 'Center latitude', 'center_latitude'),
                this.param(aspectData, 'Center longitude', 'center_longitude'),
                this.param(aspectData, 'Top-left latitude', 'top_left_latitude'),
                this.param(aspectData, 'Top-left longitude', 'top_left_longitude'),
                this.param(aspectData, 'Bottom-right latitude', 'bottom_right_latitude'),
                this.param(aspectData, 'Bottom-right longitude', 'bottom_right_longitude'),
                this.param(aspectData, 'Zoom level', 'zoom_level'),
                [$T('Default on start-up'), $B(Html.checkbox({}), aspectData.accessor('default_on_startup'))]
            ]);

            return this.ExclusivePopupWithButtons.prototype.draw.call(this, form);
        },

        _getButtons: function() {
            var self = this;
            return [
                [$T('Save'), function() {
                    self.action(self.aspectData, function() {
                        self.close();
                    });
                }],
                [$T('Cancel'), function() {
                    self.close();
                }]
            ];
        }
    },
    function(title, aspectData, action) {
        this.aspectData = aspectData;
        this.action = action;
        this.ExclusivePopupWithButtons(title);
    }
);

/**
 * Creates a list of aspects. Each aspect can be edited or removed.
 * It inherits from ListWidget who in turn inherits from WatchObject, so the usual WatchObject
 * methods (get, set) can be used on it. For example 'set' can be used to initialize the list.
 * This means that the aspects are stored with their id's as keys.
 * @param {String} style The class of the ul that will contain the aspects.
 * @param {Boolean} allowEdit. If true, each aspect will have an edit button to change their data.
 * @param {Function} editProcess. A function that will be called when a aspect is edited. The function
 *                                will be passed the new data as a WatchObject.
 */
type("MapAspectListWidget", ["ListWidget"], {

    _drawItem: function(aspect) {
        var self = this;
        var aspectData = aspect.get();

        var editButton = Widget.link(command(function() {
            var editPopup = new MapAspectDataPopup(
                'Change map aspect data',
                aspectData.clone(),
                function(newData, suicideHook) {
                    if (editPopup.parameterManager.check()) {
                        //  editProcess will be passed a WatchObject representing the aspect.
                        self.editProcess(aspectData, function(result) {
                            if (result) {
                                if (!exists(newData.get('default_on_startup'))) {
                                    newData.set('default_on_startup', false);
                                }
                                aspectData.update(newData.getAll());
                            }
                        }, newData);
                        suicideHook();
                    }
                }
            );
            editPopup.open();
        }, fossirUI.Buttons.editButton()));

        var removeButton = Widget.link(command(function() {
            // removeProcess will be passed a WatchObject representing the aspect.
            self.removeProcess(aspectData, function(result) {
                if (result) {
                    self.set(aspect.key, null);
                }
            });
        }, fossirUI.Buttons.removeButton()));

        var buttonDiv = Html.div({style: {cssFloat: 'right', paddingRight: pixels(10)}});

        buttonDiv.append(editButton) ;
        buttonDiv.append(removeButton);

        var b1 = $B(Html.span(), aspectData.accessor('name'));
        var b2 = $B(Html.span(), aspectData.accessor('default_on_startup'), function(x) {return x ? ' (' + $T('Default') + ')' : ''});

        var aspectName = Html.span({}, b1, b2);

        return Html.span({}, buttonDiv, aspectName);
    }
},

    function(style, editProcess, removeProcess) {

        this.style = any(style, "UIAspectsList");
        this.editProcess = any(editProcess, singleAspectNothing);
        this.removeProcess = any(removeProcess, singleAspectNothing);

        this.ListWidget(style);
    }
);


/**
 * Creates a form field with a list of aspects.
 */
type("MapAspectListField", ["IWidget"], {
    clear: function() {
        this.aspectList.clearList();
    },

    draw: function() {
        var self = this;
        var buttonDiv = Html.div({style:{marginTop: pixels(10)}});
        var addNewAspectButton = Html.input("button", {style: {marginRight: pixels(5)}, className: 'i-button'}, $T('Add Map Aspect') );

        addNewAspectButton.observeClick(function() {
            var newAspect = $O({});
            var newAspectPopup = new MapAspectDataPopup(
                $T('New map aspect'),
                newAspect,
                function(newData, suicideHook) {
                    if (newAspectPopup.parameterManager.check()) {
                        newAspect.update(newData.getAll());
                        if (!exists(newAspect.get('default_on_startup'))) {
                            newAspect.set('default_on_startup', false);
                        }
                        self.newProcess(newAspect, function(result) {
                            if (result.ok) {
                                newAspect.set('id', result.id)
                                self.aspectList.set(result.id, newAspect);
                            }
                        });
                        suicideHook();
                    }
                }
            );
            newAspectPopup.open();
        });
        buttonDiv.append(addNewAspectButton);

        return Widget.block([Html.div(this.aspectDivStyle, this.aspectList.draw()), buttonDiv]);

    }
},
    function(aspectDivStyle, aspectListStyle, initialAspects, newProcess, editProcess, removeProcess) {
        var self = this;
        this.aspectList = new MapAspectListWidget(aspectListStyle, editProcess, removeProcess);
        this.aspectDivStyle = any(aspectDivStyle, "UIAspectsListDiv");

        if (exists(initialAspects)) {
            each(initialAspects, function(aspect) {
                self.aspectList.set(aspect.id, $O(aspect));
            });
        }

        this.newProcess = any(newProcess, aspectListNothing);
    }
);
