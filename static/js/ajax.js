/**
 * Created by orion on 15/10/2017.
 */

'use strict';

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