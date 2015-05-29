from __future__ import absolute_import

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():
    return """
        <script>
            halloPlugins = {
        'halloformat': {},
        //'halloheadings': {formatBlocks: []},
        'hallolists': {},
        // 'hallohr': {},
        'halloreundo': {},
        'hallowagtaillink': {},
        'hallorequireparagraphs': {}
        };
        </script>
    """
