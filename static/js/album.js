/**
 * Created by orion on 22/10/2017.
 */
'use strict';

var typeaheadSettings = {
    hint: true,
    highlight: true,
    minLength: 1
};

var match = function (items) {
    return function findMatches(q, cb) {
        var matches, substrRegex;

        matches = [];
        substrRegex = new RegExp(q, 'i');
        $.each(items, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });
        cb(matches);
    };
};

function typeaheadPost(name, cmd) {
    ajaxPost({
        cmd: cmd,
        name: name,
        albumid: $('#album_id').val()
    });
    location.reload();
}

function impl_typeahead(items, $typeahead, cmd) {
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            typeaheadPost($(e.target).val(), cmd);
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function editAlbumTitle($this, albumId) {
    ajaxPost({
        cmd: 'update_album_title',
        title: $this.text().trim(),
        albumid: albumId
    });
}

function ajaxGetItems(cmdGet, nameField,  $typeahead, cmdPost) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField]);
        });
        impl_typeahead(items, $typeahead, cmdPost);
    });
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        $('.edit-title').keydown(function (e) {
            if (e.key === 'Tab') {
                editAlbumTitle($(this), albumId);
            }
        });
        ajaxGetItems('instruments', 'Name', $('.album .instrument.typeahead'), 'add_new_instrument');
        ajaxGetItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_instrument');
        ajaxGetItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_instrument');
        ajaxGetItems('tags', 'Name', $('.album .tag.typeahead'), 'add_new_instrument');

        $('.refetch').click(function(){
            const data = {
                albumid: albumId,
                cmd: 'refetch'
            };
            if (confirm("De stukken opniew ophalen?")) {
                ajaxPost(data);
                location.reload();
            }
        });
    }
    // functions for the abums list
    $('.test-scroll').click(function(){
        // test to scroll to first 'K'
        var items = $('li.hyperlink');
        items.each(function(index){
            // console.log(this);
            var $li = $(this);
            var title = $li.find('.title'),
                text = $(title).text().trim();
            // console.log(title, text);
            if (text.indexOf('44') === 0) {
                console.log(text);
                $('html, body').animate({
                    scrollTop: $(title).offset().top
                },2000);

                return false;
            }
        });
    });

});

