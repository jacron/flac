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

function play(idPiece, idAlbum) {
    const data = {
        arg: idPiece,
        cmd: 'play'
    };
    ajaxPost(data);
}

$(function() {
   $('.album-image').click(function(){
      $(this).toggleClass('expanded');
   });
   $('.edit-title').keydown(function(e) {
       const $this = $(this);
       if (e.key === 'Tab') {
           console.log($this.attr('albumid'));
           const data = {
               cmd: 'update_album_title',
               title: $this.text().trim(),
               albumid: $this.attr('albumid')
           };
           ajaxPost(data);
       }
   });
});