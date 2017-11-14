/**
 * Created by orion on 14/11/2017.
 */

'use strict';

console.log('in search');

$(function () {
    $('.search-title').keydown(function(e){
        console.log('kd');
        if (e.key === 'Enter') {
            console.log($(this).val());
            location.href = '/search/' + $(this).val();
        }
    });
});

