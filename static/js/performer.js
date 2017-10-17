/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addPerformer($select) {
    const data = {
        cmd: 'add_performer',
        performerid: $select.val(),
        albumid: $select.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function newPerformer($input) {
    const data = {
        cmd: 'new_performer',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    // console.log(data);
    ajaxPost(data);
    location.reload();
}

function removePerformer($this) {
        const data = {
        cmd: 'remove_performer',
        id: $this.attr('id'),
        albumid: $this.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

$(function() {
   $('button.select-performer').click(function () {
       addPerformer($('select.select-performer'));
   });
   $('button.add-performer').click(function() {
       newPerformer($('input.add-performer'));
   });
   $('input.add-performer').keydown(function(e) {
       if (e.key === 'Enter') {
        newPerformer($('input.add-performer'));
       }
   });
   $('select.select-performer').keydown(function(e){
       if (e.key === 'Enter') {
        addPerformer($('select.select-performer'));
       }
   });
   $('.performer .remove').click(function(){
       removePerformer($(this));
   });
});