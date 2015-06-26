from __future__ import absolute_import

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():
    return """
<script>
    $(document).ready(function(){
        $('.model-contributorpage #id_first_name').on('focus', function() {
            $('#id_slug').data('previous-val', $('#id_slug').val());
            $(this).data('previous-val', $(this).val());
        });
        $('.model-contributorpage #id_last_name').on('focus', function() {
            $('#id_slug').data('previous-val', $('#id_slug').val());
            $(this).data('previous-val', $(this).val());
        });
        $('.model-contributorpage #id_first_name').on('keyup keydown keypress blur', function() {
            if ($('body').hasClass('create') || (!$('#id_slug').data('previous-val').length || cleanForSlug($('#id_first_name').data('previous-val') + $('#id_last_name').data('previous-val')) === $('#id_slug').data('previous-val'))) {
                // only update slug if the page is being created from scratch, if slug is completely blank, or if title and slug prior to typing were identical
                $('#id_slug').val(cleanForSlug($('#id_first_name').val() + $('#id_last_name').val()));
            }
        });
    });
</script>
    """
