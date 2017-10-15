/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addComponist($select) {
    const data = {
        cmd: 'add_componist',
        componistid: $select.val(),
        albumid: $select.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function newComponist($input) {
    const data = {
        cmd: 'new_componist',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

$(function() {
   // componist
   $('button.select-componist').click(function () {
       addComponist($('select.select-componist'));
   });
   $('button.add-componist').click(function() {
       newComponist($('input.add-componist'));
   });
   $('input.add-componist').keydown(function(e) {
       if (e.key === 'Enter') {
        newComponist($('input.add-componist'));
       }
   });
   $('select.select-componist').keydown(function(e){
       if (e.key === 'Enter') {
        addComponist($('select.select-componist'));
       }
   });
});