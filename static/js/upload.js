/**
 * Created by orion on 25/11/2017.
 */
'use strict';

$(function () {
    $('.upload-album-path').keydown(function(e) {
       if (e.key === 'Enter') {
           ajaxGet({
               cmd: 'album_by_path',
               path: $(this).val()
           }, function(response) {
               console.log(response);
               $('.upload-album .title').text(response.Title);
               $('.upload-album .id').text(response.ID);
           });
       }
    });
});