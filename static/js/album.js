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
    var $typeahead = $('.album .typeahead');
    $typeahead.typeahead({
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
            var result = $('.typeahead').get(1).value;
            console.log(result);
            const data = {
                cmd: 'new_tag',
                name: result,
                albumid: $('.edit-title').attr('albumid')
            };
            ajaxPost(data);
            location.reload();
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

$(function () {
    var tags = ['test', 'test2'];
    ajaxGet({
        cmd: 'tags'
    }, function(response){
        // console.log(response);
        tags = [];
        response.forEach(function(tag) {
            tags.push(tag.Name);
        });
        // console.log(tags);
        impl_tags_typeahead(tags)
    });
});

