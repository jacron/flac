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
    var $typeahead = $('.album .componist.typeahead');
    $typeahead.typeahead({
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
            $typeahead.val('');
        }
    });
}

function impl_performers_typeahead(performers) {
    // console.log('performers', performers);
    var $typeahead = $('.album .performer.typeahead');
    $typeahead.typeahead({
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
            $typeahead.val('');
        }
    });
}

function impl_instruments_typeahead(instruments) {
    var $typeahead = $('.album .instrument.typeahead');
    $typeahead.typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            displayKey: 'Name'
        },
        {
            name: 'instruments',
            source: match(instruments)
        }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            var result = $(e.target).val();
            console.log(result);
            const data = {
                cmd: 'add_new_instrument',
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

function editAlbumTitle($this) {
    const data = {
        cmd: 'update_album_title',
        title: $this.text().trim(),
        albumid: $this.attr('albumid')
    };
    ajaxPost(data);
}

function albumDetails($target, $details) {
    if (!$target || !$target.length) { return; }

    var id = $target.attr('id'),
        title = $target.find('.title').text(),
        src = $target.find('img').attr('src');

    $details.find('a.link').attr('href', '/album/' + id + '/');
    $details.find('img').attr('src', src);
    $details.find('.title').text(title);
    $details.show();
}

$(function () {
    var tags = ['test', 'test2'];
    $('.edit-title').keydown(function (e) {
        if (e.key === 'Tab') {
            editAlbumTitle($(this));
        }
    });
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
        response.forEach(function(componist) {
            componisten.push(componist.FullName);
        });
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
        impl_performers_typeahead(performers);
    });

    var instruments = ['Piano', 'test2'];
    ajaxGet({
        cmd: 'instruments'
    }, function(response){
        instruments = [];
        response.forEach(function(instrument) {
            instruments.push(instrument.Name);
        });
        impl_instruments_typeahead(instruments);
    });

    $('.album-list .hyperlink').click(function(e){
        var $target = $(e.target).parents('li'),
            $details = $('.album-details');

        albumDetails($target, $details);
        $('body').keydown(function(e){
           switch(e.key) {
               case 'ArrowRight':
                   var $next = $target.next();
                   if ($next.length) {
                       $target = $next;
                       albumDetails($target, $details);
                   }
                   break;
               case 'ArrowLeft':
                   var $prev = $target.prev();
                   if ($prev.length) {
                       $target = $prev;
                       albumDetails($target, $details);
                   }
                   break;
               case 'Escape':
                   $details.hide();
                   break;
           }
        });
    });
});

