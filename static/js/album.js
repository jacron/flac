/**
 * Created by orion on 22/10/2017.
 */
'use strict';

function editAlbumTitle($this, albumId) {
    ajaxPost({
        cmd: 'update_album_title',
        title: $this.text().trim(),
        albumid: albumId
    });
}

function refetch() {
    ajaxPost({
        albumid: $('#album_id').val(),
        cmd: 'refetch'
    }, function(){
        location.reload();
    });
}

$(function () {
    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        $('.edit-title').keydown(function (e) {
            if (e.key === 'Tab') {
                editAlbumTitle($(this), albumId);
            }
        });
        $('.refetch').click(function(){
            // if (confirm("De stukken opniew ophalen?"))
            {
                refetch();
            }
        });
    }

});

