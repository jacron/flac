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
               if (response.Title) {
                   $('.upload-album .title').text(response.Title);
                   $('.upload-album .id')
                        .text(response.ID)
                        .attr('id', response.ID);
                   $('.upload-controls .autofill').addClass('active');
               }
           });
       }
    });
    $('.upload-controls .autofill').click(function(e) {
        var albumId = $('.upload-album .id').attr('id');
        if (albumId) {
            var li = $(this).parents('li').first();
            var elm = li.attr('class');
            var input = li.find('input');
            ajaxGet({
                cmd: 'element',
                albumid: $('.upload-album .id').attr('id'),
                name: elm
            }, function(response) {
                console.log(response);
                if (response) {
                    input.val(response);
                }
            });
        }
    });
});