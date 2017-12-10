/**
 * Created by orion on 12/11/2017.
 */

'use strict';

var typeaheadSettings = {
    hint: true,
    highlight: true,
    minLength: 1,
    // limit: 10,
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

function impl_post_typeahead(items, $typeahead, cmd) {
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

function query() {
    var q = '';
    const qComponist = $('.search .componist .typeahead.tt-input').val(),
        qTag = $('.search .tag .typeahead.tt-input').val(),
        qPerformer = $('.search .performer .typeahead.tt-input').val(),
        qInstrument = $('.search .instrument .typeahead.tt-input').val();
    console.log(qComponist);
    if (qComponist.length) {
        q = 'componist=' + getId(qComponist);
    }
    if (qPerformer.length) {
        if (q.length) { q += '&';}
        q += 'performer=' + getId(qPerformer);
    }
    if (qTag.length) {
        if (q.length) { q += '&';}
        q += 'tag=' + getId(qTag);
    }
    if (qInstrument.length) {
        if (q.length) { q += '&';}
        q += 'instrument=' + getId(qInstrument);
    }
    if (q.length) { q = '?' + q;}
    // console.log(q);
    document.location.href = '/search' + q;
}

function impl_query_typeahead(items, type) {
    const $typeahead = $('.upload-controls .' + type + ' .typeahead');
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            // console.log(getId($typeahead.val()));
            $('.search input[name=' + type + ']').val(getId($typeahead.val()))
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function impl_typeahead(items, $typeahead) {
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function typeAheadAlbumItems(cmdGet, nameField, $typeahead, cmdPost) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField]);
        });
        impl_post_typeahead(items, $typeahead, cmdPost);
    });
}

function typeAheadUpload(cmdGet, nameField, $typeahead) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField] + '_' + item.ID);
        });
        impl_typeahead(items, $typeahead);
    });
}

function typeAheadSearch(cmdGet, nameField, type) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField] + '_' + item.ID);
        });
        impl_query_typeahead(items, type);
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
            albumIds = [];
            return $.map(response, function(movie) {
                albumIds.push(movie.ID);
                const name = movie.name + ' - ' + movie.ID;
                return {name:name};
            });
        }
    }
});

var albumIds = [];

function getId(s) {
    var pos = s.lastIndexOf('_');
    return s.substr(pos + 1);
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
            // const id = getId($(e.target).val());
            console.log(albumIds);
            // location.href = '/album/' + id;
        }
    });
}

function searchTagsTypeahead($typeahead, cmdGet, nameField) {
    ajaxGet({
        cmd: cmdGet
    }, function(response){
        var items = [];
        response.forEach(function(item) {
            items.push(item[nameField]);
        });
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).keydown(function(e){

        });
    });
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        typeAheadAlbumItems('instruments', 'Name', $('.album .instrument.typeahead'), 'add_new_instrument');
        typeAheadAlbumItems('performers', 'FullName', $('.album .performer.typeahead'), 'add_new_performer');
        typeAheadAlbumItems('componisten', 'FullName', $('.album .componist.typeahead'), 'add_new_componist');
        typeAheadAlbumItems('tags', 'Name', $('.album .tag.typeahead'), 'new_tag');
    }
    quickSearch($('.performer-naam'), $('.performers .typeahead'), '/performer/', 'performerid');
    quickSearch($('.componist-naam'), $('.componisten .typeahead'), '/componist/', 'componistid');
    generalSearch($('.typeahead.general'));
    searchTagsTypeahead($('.search .tag.typeahead'), 'tags', 'Name');
    if ($('.upload-album-path').length) {
        // functions for the upload page
        typeAheadUpload('instruments', 'Name',
            $('.upload-controls .instrument .typeahead'));
        typeAheadUpload('performers', 'FullName',
            $('.upload-controls .performer .typeahead'));
        typeAheadUpload('componisten', 'FullName',
            $('.upload-controls .componist .typeahead'));
        typeAheadUpload('tags', 'Name',
            $('.upload-controls .tag .typeahead'));
    }
    if ($('.search').length) {
        // functions for the searcvh page
        typeAheadSearch('instruments', 'Name', 'instrument');
        typeAheadSearch('performers', 'FullName', 'performer');
        typeAheadSearch('componisten', 'FullName', 'componist');
        typeAheadSearch('tags', 'Name', 'tag');
        $('.do-search').click(function() {
            query();
        });
    }
});



