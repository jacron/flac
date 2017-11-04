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
    const albumId = $('#album_id').val();
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
                albumid: albumId
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
    const albumId = $('#album_id').val();
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
                albumid: albumId
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
    var $typeahead = $('.album .performer.typeahead');
    const albumId = $('#album_id').val();
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
                albumid: albumId
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
    const albumId = $('#album_id').val();
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
                albumid: albumId
            };
            ajaxPost(data);
            location.reload();
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function editAlbumTitle($this, albumId) {
    const data = {
        cmd: 'update_album_title',
        title: $this.text().trim(),
        albumid: albumId
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

    const albumId = $('#album_id').val();

    var tags = ['test', 'test2'];
    $('.edit-title').keydown(function (e) {
        if (e.key === 'Tab') {
            editAlbumTitle($(this), albumId);
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

    $('.refetch').click(function(e){
        // const albumId = $('#album_id').val();
        const data = {
            albumid: albumId,
            cmd: 'refetch'
        };
        if (confirm("De stukken opniew ophalen?")) {
            ajaxPost(data);
            location.reload();
        }
    });
    // $('body').keydown(function(e){
    //     if ($('.album').length) {
    //         const albumId = $('#album_id').val();
           //  switch(e.key) {
           //     case 'ArrowRight':
           //         document.location.href = '/next/' + albumId + '/';
           //         break;
           //     case 'ArrowLeft':
           //         document.location.href = '/prev/' + albumId + '/';
           //         break;
           // }
        // }
    // });
});

