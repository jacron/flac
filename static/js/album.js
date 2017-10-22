/**
 * Created by orion on 22/10/2017.
 */
'use strict';

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

function impl_performers_typeahead(performers) {
    var $tagTypeahead = $('.album .performer.typeahead');
    $tagTypeahead.typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            displayKey: 'Name'
        },
        {
            name: 'performers',
            source: match(performers)
        }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            var result = $(e.target).val();
            console.log(result);
            const data = {
                cmd: 'add_new_performer',
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
    var performers = ['Paul van Nevel', 'test2'];
    ajaxGet({
        cmd: 'performers'
    }, function(response){
        performers = [];
        response.forEach(function(performer) {
            performers.push(performer.FullName);
        });
        // console.log(performers);
        impl_performers_typeahead(performers);
    });
});

