function initModal(modal) {

    function ajaxifyLinks(context) {
        $('a.endnote-choice', modal.body).click(function() {
            modal.loadUrl(this.href);
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute('data-page');
            setPage(page);
            return false;
        });
    }

    var searchUrl = $('form.endnote-search', modal.body).attr('action');

    function search() {
        $.ajax({
            url: searchUrl,
            data: {q: $('#id_q').val(), results: 'true'},
            success: function(data, status) {
                $('#search-results').html(data);
                ajaxifyLinks($('#search-results'));
            }
        });
        return false;
    }

    function setPage(page) {
        var dataObj = {p: page, results: 'true'};

        if ($('#id_q').length && $('#id_q').val().length) {
            dataObj.q = $('#id_q').val();
        }

        $.ajax({
            url: searchUrl,
            data: dataObj,
            success: function(data, status) {
                $('#search-results').html(data);
                ajaxifyLinks($('#search-results'));
            }
        });
        return false;
    }

    $('form.endnote-search', modal.body).submit(search);

    $('#id_q').on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 50);
        $(this).data('timer', wait);
    });

    ajaxifyLinks(modal.body);
}
