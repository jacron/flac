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