

type("RoomListWidget", ["ListWidget"],
    {
        _drawItem: function(room) {
            var self = this;
            var roomData = room.get();

            var removeButton = Widget.link(command(function() {
                self.removeProcess(room.key, function(result) {
                    if (result) {
                        self.set(room, null);
                    }
                });
            }, fossirUI.Buttons.removeButton()));
            return Html.div({style:{display: 'inline'}},
                            Html.span({},
                                    Html.div({style: {cssFloat: "right", paddingRight: "10px"}},removeButton),
                                    $B(Html.span(), self.useValue ? roomData : room.key)
                                    ));
        }
    },

    function(style, removeProcess, useValue) {
        this.removeProcess = removeProcess;
        this.useValue = useValue || false;
        if (!exists(style)) {
            style = "user-list";
        }
        this.ListWidget(style);
    }
);
