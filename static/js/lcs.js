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
                        return false;  // break each()
                    }
                });
                return false;  // break each()
            }
        });
        if (temp_common !== '' && temp_common.length > common.length) {
            common = temp_common;
        }
    }
    return common;
}

$(function () {
});