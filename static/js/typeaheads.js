/**
 * Created by orion on 12/11/2017.
 */

'use strict';

var typeaheadSettings = {
    hint: true,
    highlight: true,
    minLength: 2,
    limit: 10,
    name: 'name'
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

function typeaheadAlbumComponisten($typeahead, $makeCuesheet) {
    const items = getAlbumComponisten();
    if (items.length === 1) {$typeahead.val(items[0]); }
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            copyComponist($typeahead.val(), $makeCuesheet);
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function goResult($naam, val, href, attrId) {
    $naam.each(function () {
        var $this = $(this);
        if ($this.text() === val) {
            location.href = href + $this.attr(attrId);
        }
    });
}

function quickSearch($naam, $typeahead, href, attrId) {
    var items = [];
    $naam.each(function () {
        items.push($(this).text());
    });
    $typeahead.typeahead(
        typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            goResult($naam, $typeahead.val(), href, attrId);
        }
    });
}

//https://stackoverflow.com/questions/21530063/how-do-we-set-remote-in-typeahead-js
var albums = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        wildcard: '%QUERY',
        url: '/ajax/?cmd=generalsearch&query=%QUERY',
        transform: function(response) {
            // console.log(response);
            return $.map(response, function(movie) {
                const name = movie.name + ' - ' + movie.ID;
                return {name:name};
            });
        }
    }
});

function getId(s) {
    var pos = s.indexOf(' - ');
    return s.substr(pos + 3);
}

function generalSearch($typeahead) {
    $typeahead.typeahead(
        typeaheadSettings,
        {
            displayKey: 'name',
            source: albums,
            updater: function(item) {
                console.log(item);
                return item;
            }
        }).keydown(function(e) {
        if (e.key === 'Enter') {
            // console.log($(e.target).val());
            const id = getId($(e.target).val());
            console.log(id);
            location.href = '/album/' + id;
        }
    });
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        ajaxGetItems('instruments', 'Name', $('.album .instrument.typeahead'), 'add_new_instrument');
        ajaxGetItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_performer');
        ajaxGetItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_componist');
        ajaxGetItems('tags', 'Name', $('.album .tag.typeahead'), 'new_tag');
    }
    quickSearch($('.performer-naam'), $('.performers .typeahead'), '/performer/', 'performerid');
    quickSearch($('.componist-naam'), $('.componisten .typeahead'), '/componist/', 'componistid');
    generalSearch($('.typeahead.general'));
});



