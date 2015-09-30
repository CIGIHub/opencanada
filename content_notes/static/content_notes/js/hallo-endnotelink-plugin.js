(function () {
    (function ($) {
        return $.widget('IKS.halloendnotelink', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;

                widget = this;

                getEnclosingLink = function() {
                    var node;

                    node = widget.options.editable.getSelection().commonAncestorContainer;
                    return $(node).parents('span').get(0);
                };

                button = $('<span></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Pop-Up End Note Link',
                    icon: 'fa fa-external-link-square',
                    command: null,
                    queryState: function(event) {
                        return button.hallobutton('checked', !!getEnclosingLink());
                    }
                });
                toolbar.append(button);
                return button.on('click', function(event) {
                    var enclosingLink, lastSelection, url;

                    enclosingLink = getEnclosingLink();
                    if (enclosingLink){
                        $(enclosingLink).replaceWith(enclosingLink.innerHTML);
                        button.hallobutton('checked', false);
                        return widget.options.editable.element.trigger('change');
                    } else {

                        lastSelection = widget.options.editable.getSelection();
                        if (lastSelection.collapsed) {
                            url = window.chooserUrls.endNoteChooser;
                        } else {
                            url = window.chooserUrls.endNoteChooser;
                        }
                    }

                    return ModalWorkflow({
                        url: url,
                        responses: {
                            endnoteChosen: function(itemData) {
                                var elem;

                                elem = document.createElement('sup');
                                elem.setAttribute('data-toggle', 'modal');
                                if (itemData.id){
                                    elem.setAttribute('data-target', '#endNoteModal' + itemData.id);
                                    elem.setAttribute('data-reference', itemData.id);
                                }
                                $(elem).addClass('modal-link clickable endnote-link');

                                if ((!lastSelection.collapsed) && lastSelection.canSurroundContents()) {
                                    lastSelection.surroundContents(elem);
                                } else {
                                    elem.appendChild(document.createTextNode("endnote"));
                                    lastSelection.insertNode(elem);
                                }

                                return widget.options.editable.element.trigger('change');
                            }
                        }
                    });
                });
            }
        });
    })(jQuery);

}).call(this);
