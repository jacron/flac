/**
 * Created by orion on 08/10/2017.
 */
'use strict';
// console.log('hello piece!');

function play(file, csrf_token) {
    // console.log(file);
    var url = 'http://dev.movies13/?post=open_program';
    url = '/ajax/';
    console.log(url);
    const data = {
        program: encodeURI('media center 21'),
        args: encodeURI(file)
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