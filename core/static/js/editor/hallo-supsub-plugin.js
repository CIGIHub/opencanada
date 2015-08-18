(function() {
    (function($) {
        return $.widget('IKS.hallosupsub', {
            options: {
                editable: null,
                uuid: '',
                formattings: {
                  superscript: true,
                  subscript: true
                },
                buttonCssClass: null
              },
              populateToolbar: function(toolbar) {
                  var buttonize, buttonset, enabled, format, widget, _ref,
                      _this = this;
                  widget = this;
                  buttonset = jQuery("<span class=\"" + widget.widgetName + "\"></span>");
                  buttonize = function (format) {
                      var buttonHolder;
                      buttonHolder = jQuery('<span></span>');
                      buttonHolder.hallobutton({
                          label: format,
                          editable: _this.options.editable,
                          command: format,
                          uuid: _this.options.uuid,
                          cssClass: _this.options.buttonCssClass,
                          icon: 'fa fa-' + format
                      });
                      return buttonset.append(buttonHolder);
                  };
                  _ref = this.options.formattings;
                  for (format in _ref) {
                      enabled = _ref[format];
                      if (!enabled) {
                          continue;
                      }
                      buttonize(format);
                  }
                  buttonset.hallobuttonset();
                  return toolbar.append(buttonset);
              }
        });
    })(jQuery);

}).call(this);
