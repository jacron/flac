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
        // $.each(items, function (i, str) {
        //     if (str.indexOf(q) !== -1) {
        //         matches.push(str);
        //     }
        // });

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
    // console.log('items', items);
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

function refetch() {
    ajaxPost({
        albumid: $('#album_id').val(),
        cmd: 'refetch'
    }, function(){
        location.reload();
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
        ajaxGetItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_performer');
        ajaxGetItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_componist');
        ajaxGetItems('tags', 'Name', $('.album .tag.typeahead'), 'new_tag');

        $('.refetch').click(function(){
            // if (confirm("De stukken opniew ophalen?"))
            {
                refetch();
            }
        });
    }

});

