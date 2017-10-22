/**
 * Created by orion on 22/10/2017.
 */
'use strict';

var match = function (items) {
    return function findMatches(q, cb) {
        var matches, substrRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(items, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });

        cb(matches);
    };
};


function impl_tags_typeahead(tags) {
    var $tagTypeahead = $('.album .tag.typeahead');
    $tagTypeahead.typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            displayKey: 'Name'
        },
        {
            name: 'tags',
            source: match(tags)
        }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            var result = $(e.target).val();
            // console.log(result);
            const data = {
                cmd: 'new_tag',
                name: result,
                albumid: $('.edit-title').attr('albumid')
            };
            ajaxPost(data);
            location.reload();
        }
        if (e.key === 'Escape') {
            $tagTypeahead.val('');
        }
    });
}

function impl_componisten_typeahead(componisten) {
    var $tagTypeahead = $('.album .componist.typeahead');
    $tagTypeahead.typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            displayKey: 'Name'
        },
        {
            name: 'componisten',
            source: match(componisten)
        }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            var result = $(e.target).val();
            console.log(result);
            const data = {
                cmd: 'add_new_componist',
                name: result,
                albumid: $('.edit-title').attr('albumid')
            };
            ajaxPost(data);
            location.reload();
        }
        if (e.key === 'Escape') {
            $tagTypeahead.val('');
        }
    });
}

$(function () {
    var tags = ['test', 'test2'];
    ajaxGet({
        cmd: 'tags'
    }, function(response){
        tags = [];
        response.tags.forEach(function(tag) {
            tags.push(tag.Name);
        });
        impl_tags_typeahead(tags);
    });
    var componisten = ['Bach JS', 'test2'];
    ajaxGet({
        cmd: 'componisten'
    }, function(response){
        componisten = [];
        // console.log(response);
        response.forEach(function(componist) {
            componisten.push(componist.FullName);
        });
        // console.log(componisten);
        impl_componisten_typeahead(componisten);
    });
});

