/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    $('.search-title').keydown(function(e){
        if (e.key === 'Enter') {
            // console.log($(this).val());
            location.href = '/search/' + $(this).val();
        }
    });
    $('.search-inside-componist').keydown(function(e){
        if (e.key === 'Enter') {
            // console.log($(this).val());
            location.href = '/componist/' + $('#componist_id').val() + '/search/' +
                $(this).val() + '/';
        }
    });
});

