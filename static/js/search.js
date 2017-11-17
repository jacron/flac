/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    $('.search-title').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/search/' + $(this).val();
        }
    });
    $('.search-inside-componist').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/componist/' + $('#componist_id').val() + '/search/' +
                $(this).val() + '/';
        }
    });
    $('.search-inside-collection').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/collection/' + $(this).val() + '/search';
        }
    });
    $('.search-inside-instrument').keydown(function(e){
        if (e.key === 'Enter') {
            location.href = '/instrument/' + $('#instrument_id').val() + '/search/' + $(this).val();
        }
    });
});

