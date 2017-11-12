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
    ajaxPost(data);
    location.reload();
}

function removePerformer($this) {
        const data = {
        cmd: 'remove_performer',
        id: $this.attr('id'),
        albumid: $('#album_id').val()
    };
    ajaxPost(data);
    location.reload();
}

function editPerformerName($this) {
    const data = {
        cmd: 'update_performer_name',
        name: $this.text().trim(),
        id: $this.attr('performer_id')
    };
    ajaxPost(data);
}

function editPerformerYears($this) {
    const data = {
        cmd: 'update_performer_years',
        years: $this.text().trim(),
        id: $this.attr('performer_id')
    };
    ajaxPost(data);
}

$(function() {
    // performer
    $('.edit-performer-name').keydown(function (e) {
        if (e.key === 'Tab') {
            editPerformerName($(this));
        }
    });
    $('.edit-performer-years').keydown(function (e) {
        if (e.key === 'Tab') {
            editPerformerYears($(this));
        }
    });
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
    $('.add-performer').click(function(e) {
        var $target = $(e.target),
            id = $target.attr('id'),
            albumId = $('#album_id').val();
        const data = {
            cmd: 'add_performer',
            performerid: id,
            albumid: albumId
        };
        ajaxPost(data);
        location.reload();
    });
    const performer_id = $('#performer_id').val();
    handleDrop($('#drop-area-performer'), performer_id, 'performer_id');
    preventSpilledDrop($('.performer'));
});