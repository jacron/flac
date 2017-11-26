/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function ajaxGet(data, cb) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        type: 'GET',
        url: url,
        data: data,
        headers: headers,
        dataType: 'json'
    }).done(function(response){
        cb(response);
    }).fail(function(err) {
        cb(err.responseText);
    });
}

function ajaxPost(data, cb) {
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
        if (cb) {
            cb(response);
        }
    }).fail(function(err) {
        console.log(err);
        if (cb) {
            cb(err);
        }
    });
}

function openfinder(objectId, kind) {
    ajaxPost({
        objectid: objectId,
        cmd: 'openfinder',
        kind: kind
    });
}

function openwebsite(albumId) {
    ajaxPost({
        cmd: 'openwebsite',
        albumid: albumId
    })
}

function play(idPiece) {
    ajaxPost({
        arg: idPiece,
        cmd: 'play'
    });
}

function postMakeCuesheet(name, ids, cb) {
    ajaxPost({
        cmd: 'makecuesheet',
        ids: ids,
        name: name,
        albumid: $('#album_id').val()
    }, function(response){if (cb) {cb(response);}})
}

function postRenameCuesheet(pieceId, albumId, cb) {
    ajaxPost({
        cmd: 'renamecue',
        id: pieceId,
        albumid: albumId
    }, function(response){if (cb) {cb(response);}})
}

function refetch() {
    ajaxPost({
        albumid: $('#album_id').val(),
        cmd: 'refetch'
    }, function(){
        location.reload();
    });
}

