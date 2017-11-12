/**
 * Created by orion on 12/11/2017.
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

function getAlbumItems($typeahead, $makeCuesheet) {
    var items = [];
    var $hyperlinkComponist = $('li.hyperlink.componist');
    $.each($hyperlinkComponist, function(key, li){
        items.push($(li).find('a').text().trim());
    });
    if (items.length == 1) {$typeahead.val(items[0]); }
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            const name = $(e.target).val();
            $makeCuesheet.val(name + $makeCuesheet.val());
            $typeahead.val('');
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

$(function () {
    const albumId = $('#album_id').val();
    const $selectForCuesheet = $('.select-for-cuesheet'),
          $makeCuesheet = $('.make-cuesheet'),
          $typeahead = $('.album-componist.typeahead');
    if (albumId) {
        // functions for the single album page
        ajaxGetItems('instruments', 'Name', $('.album .instrument.typeahead'), 'add_new_instrument');
        ajaxGetItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_performer');
        ajaxGetItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_componist');
        ajaxGetItems('tags', 'Name', $('.album .tag.typeahead'), 'new_tag');
        getAlbumItems($typeahead, $('.make-cuesheet'));
        $('.album-componist-to-make').click(function(){
            $makeCuesheet.val($typeahead.val() + $makeCuesheet.val());
        });
    }
});



