/**
 * Created by orion on 12/11/2017.
 */

'use strict';

function getSmallest(lines) {
    var small = '';
    lines.forEach(function(line){
        if (small.length < line.length) {
            small = line;
        }
    });
    return small;
}

function lcs(lines) {
    var common = '';
    var small = getSmallest(lines);
    var temp_common = '';
    for (var i=0; i< small.length; i++) {
        var c = small[i];
        temp_common += c;
        $.each(lines, function(key, line) {
            if (line.indexOf(temp_common) === -1) {
                temp_common = c;
                $.each(lines, function(key2, line2) {
                    if (line2.indexOf(temp_common) === -1) {
                        temp_common = '';
                        return false;
                    }
                });
                return false;
            }
        });
        if (temp_common !== '' && temp_common.length > common.length) {
            common = temp_common;
        }
    }
    return common;
}

function similar($selectForCuesheet) {
    var titles = [];
    var common = '';
    var active = false;
    var old_common = '';
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            active = true;
        }
        if (active) {
            val.checked = true;
            titles.push(titleOfPiece($(val)));
            common = lcs(titles);
            if (titles.length > 2 && common.length < old_common.length - 2) {
                titles.pop();
                val.checked = false;
                return false;
            }
            old_common = common;
        }
    });
    return titles;
}

function lcs_pieces($selectForCuesheet, $makeCuesheet){
    var titles = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            titles.push(titleOfPiece($(val)));
        }
    });
    if (titles.length === 1) {
        titles = similar($selectForCuesheet);
    }
    var common = lcs(titles);
    if (common.substr(common.length-1) == 'I') {
        common = common.substr(0, common.length-1);
    }
    $makeCuesheet.val(common);
}

$(function () {
    const $selectForCuesheet = $('.select-for-cuesheet'),
          $makeCuesheet = $('.make-cuesheet');
    $('.test-lcs').click(function(){
        lcs_pieces($selectForCuesheet, $makeCuesheet);
    });
});