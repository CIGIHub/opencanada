function(modal) {
    modal.respond('endnoteChosen', {{ endnote_json|safe }});
    modal.close();
}
