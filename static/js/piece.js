/**
 * Created by orion on 08/10/2017.
 */
'use strict';
// console.log('hello piece!');

function ajaxPost(data) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        headers: headers,
        dataType: 'json'
    }).done(function(response){
        console.log(response);
    }).fail(function(err) {
        console.log(err.responseText);
    });
}

function openfinder(albumId) {
    const data = {
        arg: albumId,
        cmd: 'openfinder'
    };
    ajaxPost(data);
}

function play(idPiece) {
    const data = {
        arg: idPiece,
        cmd: 'play'
    };
    ajaxPost(data);
}

function editAlbumTitle($this) {
   const data = {
       cmd: 'update_album_title',
       title: $this.text().trim(),
       albumid: $this.attr('albumid')
   };
   ajaxPost(data);
}

function addComponist($select) {
    const data = {
        cmd: 'add_componist',
        componistid: $select.val(),
        albumid: $select.attr('albumid')
    };
    // console.log(data);
    ajaxPost(data);
    location.reload();
}

function newComponist($input) {
    const data = {
        cmd: 'new_componist',
        name: $input.val()
    };
    // console.log(data);
    ajaxPost(data);
    location.reload();
}

function toggleContent($this, parent, sibling) {
    const next = $this.parents(parent).siblings(sibling);
    if ($this.hasClass('fa-caret-up')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-up');
        next.show();
    } else {
        $this.addClass('fa-caret-up');
        $this.removeClass('fa-caret-down');
        next.hide();
    }
}

$(function() {
   $('.album-image').click(function(){
      $(this).toggleClass('expanded');
   });
   $('.edit-title').keydown(function(e) {
       if (e.key === 'Tab') {
           editAlbumTitle($(this));
       }
   });
   $('.toggle-content').click(function(){
       toggleContent($(this), 'h4', 'table');
   });
   $('.toggle-edit').click(function(){
       toggleContent($(this), 'h4', '.content.edit');
   });
   $('button.select-componist').click(function () {
       addComponist($('select.select-componist'));
   });
   $('button.add-componist').click(function() {
       newComponist($('input.add-componist'));
   });
   $('input.add-componist').keydown(function(e) {
       if (e.key == 'Enter') {
        newComponist($('input.add-componist'));
       }
   });
   $('select.select-componist').keydown(function(e){
       if (e.key == 'Enter') {
           addComponist($('select.select-componist'));
       }
   });
});