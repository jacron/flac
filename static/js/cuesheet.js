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

function getAlbumComponisten($typeahead) {
    var items = [];
    $.each($('li.hyperlink.componist'), function(key, li){
        items.push($(li).find('a').text().trim());
    });
    if (items.length === 1) {$typeahead.val(items[0]); }
    return items;
}

function typeaheadAlbumComponisten($typeahead, $makeCuesheet) {
    const items = getAlbumComponisten($typeahead);
    $typeahead.typeahead(typeaheadSettings,
        { source: match(items) }
    ).keydown(function(e){
        if (e.key === 'Enter') {
            $makeCuesheet.val($(e.target).val() + $makeCuesheet.val());
            $typeahead.val('');
        }
        if (e.key === 'Escape') {
            $typeahead.val('');
        }
    });
}

function copyComponist(componist, $makeCuesheet) {
    const normalizedComponist = componist.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    $makeCuesheet.val(normalizedComponist + $makeCuesheet.val());
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        const $selectForCuesheet = $('.select-for-cuesheet'),
            $makeCuesheet = $('.make-cuesheet'),
            $typeahead = $('.album-componist.typeahead');
        var cusheetIds = [];

        $selectForCuesheet.click(function (e) {
            if (e.shiftKey) {
                selectSiblingsInBetween($selectForCuesheet);
            }
            cusheetIds = getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet);
        });
        $makeCuesheet.keydown(function (e) {
            if (e.key === 'Enter') {
                postMakeCuesheet($(e.target).val(), cusheetIds);
            }
        });
        $('.stukken .check-all').click(function () {
            cusheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, true);
        });
        $('.stukken .check-nothing').click(function () {
            cusheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, false);
        });
        typeaheadAlbumComponisten($typeahead, $makeCuesheet);
        $('.album-componist-to-make').click(function () {
            copyComponist($typeahead.val(), $makeCuesheet);
        });
        $('.create-cuesheet').click(function(){
            postMakeCuesheet($makeCuesheet.val(), cusheetIds, function(response) {});
        });
        $('.rename-cuesheet').click(function(){
            postRenameCuesheet(this.id, $('#album_id').val(), function(response) {
                location.reload();
            });
        });
    }
});