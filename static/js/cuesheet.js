/**
 * Created by orion on 08/10/2017.
 */
'use strict';

function titleOfPiece($val) {
    var parent = $val.parents('.hyperlink').first();
    return parent.find('a').first().text();
}

function getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            if (!active) {
                // first time making active true
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
            }
            active = true;
            ids.push(val.id);
        }
    });
    return ids;
}

function selectSiblingsInBetween($selectForCuesheet) {
    // if between checked items there are unchecked, check them
    var keys = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            keys.push(key);
        }
    });
    if (keys.length > 1) {
        for (var i = 1; i < keys.length; i++) {
            if (keys[i] - keys[i-1] > 1) {
                for (var j = keys[i-1] + 1; j < keys[i]; j++) {
                    $selectForCuesheet.get(j).checked = true;
                }
            }
        }
    }
}

function selectCheckboxes($selectForCuesheet, $makeCuesheet, mode) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        val.checked = mode;
        if (mode) {
            ids.push(val.id);
            if (!active) {
                // first time making active true: use title of piece for cuesheet title
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
                active = true;
            }
        }
    });
    return ids;
}

function getAlbumComponisten() {
    var items = [];
    $.each($('li.hyperlink.componist'), function(key, li){
        items.push($(li).find('a').text().trim());
    });
    return items;
}

function typeaheadAlbumComponisten($typeahead, $makeCuesheet) {
    const items = getAlbumComponisten();
    if (items.length === 1) {$typeahead.val(items[0]); }
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            copyComponist($typeahead.val(), $makeCuesheet);
            // $typeahead.val('');
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function copyComponist(componist, $makeCuesheet) {
    const normalizedComponist = componist.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    var val = $makeCuesheet.val();
    if (val[0] !== ' ' && val[0] !== '-') {val = ' - ' + val;}
    $makeCuesheet.val(normalizedComponist + val);
}

function similar($selectForCuesheet) {
    var titles = [];
    var ids = [];
    var common = '';
    var active = false;
    var old_common = '';
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            active = true;
        }
        if (active) {
            val.checked = false;
            ids.push(val.id);
            titles.push(titleOfPiece($(val)));
            common = lcs(titles);
            if (titles.length > 2 && common.length < old_common.length - 2) {
                titles.pop();
                ids.pop();
                val.checked = true;
                return false;  // break each()
            }
            old_common = common;
        }
    });
    return {
        titles: titles,
        ids: ids
    };
}

function trimNr(s) {
    if (s.substr(s.length-1) === 'I') {
        return s.substr(0, s.length-1);
    }
    return s;
}

function lcs_pieces($selectForCuesheet, $makeCuesheet){
    var titles = [];
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            titles.push(titleOfPiece($(val)));
            ids.push(val.id);
        }
    });
    if (titles.length === 1) {
        const data = similar($selectForCuesheet);
        titles = data.titles;
        ids = data.ids;
    }
    $makeCuesheet.val(trimNr(lcs(titles)));
    return ids;
}

function afterPostMake($makeCuesheet, $typeahead) {
    // location.reload()
    $makeCuesheet.val('');
    var items = getAlbumComponisten();
    if (items.length === 1) {$typeahead.val(items[0]); }
    else { $typeahead.val('')};
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        const $selectForCuesheet = $('.select-for-cuesheet'),
            $makeCuesheet = $('.make-cuesheet'),
            $typeahead = $('.album-componist.typeahead');
        var cuesheetIds = [];

        $selectForCuesheet.click(function (e) {
            if (e.shiftKey) {
                selectSiblingsInBetween($selectForCuesheet);
            }
            cuesheetIds = getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet);
        });
        $makeCuesheet.keydown(function (e) {
            if (e.key === 'Enter') {
                postMakeCuesheet($(e.target).val(), cuesheetIds, function(response) {
                    afterPostMake($makeCuesheet, $typeahead)});
            }
        });
        $('.test-lcs').click(function(){
            cuesheetIds = lcs_pieces($selectForCuesheet, $makeCuesheet);
        });
        typeaheadAlbumComponisten($typeahead, $makeCuesheet);
        $('.album-componist-to-make').click(function () {
            copyComponist($typeahead.val(), $makeCuesheet);
        });
        $('.create-cuesheet').click(function(){
            postMakeCuesheet($makeCuesheet.val(), cuesheetIds, function(response) {
                afterPostMake($makeCuesheet, $typeahead)});
        });
        $('.rename-cuesheet').click(function(){
            postRenameCuesheet(this.id, $('#album_id').val(), function(response) {
                location.reload();
            });
        });
        $('.stukken .check-all').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, true);
        });
        $('.stukken .check-nothing').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, false);
        });
    }
});