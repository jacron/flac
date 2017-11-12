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
            var result = $('.typeahead').get(1).value;
            $naam.each(function () {
                var $this = $(this);
                if ($this.text() === result) {
                    location.href = href + $this.attr(attrId);
                }
            });
        }
    });

}

var movies = new Bloodhound({
    datumTokenizer: function (datum) {
        return Bloodhound.tokenizers.whitespace(datum.value);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        wildcard: '%QUERY',
        url: '/ajax/?cmd=generalsearch&query=%QUERY',
        transform: function(response) {
            console.log(response);
            return $.map(response, function(movie) {
                return {name:movie.name};
            });
        }
    }
});

function generalSearch($typeahead) {
    $typeahead.typeahead(
        typeaheadSettings,
        {
            displayKey: 'name',
            source: movies
            // source: function(query, process) {
            //     const data = {cmd:'generalsearch', query: query};
            //     // return $.get('/ajax/', data, function(response) {
            //     //     console.log(response);
            //     //     const data = $.parseJSON(response);
            //     //     return process(JSON.parse(data));
            //     // });
            //     return ajaxGet(data, function(response) {
            //         console.log(response);
            //         // var items = [];
            //         // response.forEach(function(item) {
            //         //     items.push(item.name);
            //         // });
            //         // console.log(items);
            //         return process(response);
            // })
        // }
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



