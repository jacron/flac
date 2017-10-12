/**
 * Created by orion on 08/10/2017.
 */
'use strict';
// console.log('hello piece!');

function ajaxPost(cmd, arg) {
    const url = '/ajax/';
    console.log(url);
    const data = {
        arg: arg,
        cmd: cmd
    };
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
        console.log(err);
    });
}

function openfinder(albumId) {
    console.log(albumId);
    ajaxPost('openfinder', albumId);
}

function play(idPiece, idAlbum) {
    // var url = 'http://dev.movies13/?post=open_program';
    ajaxPost('play', idPiece);
}