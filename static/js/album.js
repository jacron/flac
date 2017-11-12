/**
 * Created by orion on 22/10/2017.
 */
'use strict';

function getTitle($this) {
    const parent = $this.parents('.cue-header').find('span').first();
    return parent.text();
}

function copyTitle($this) {
    const title = getTitle($this),
        $title = $('.edit-title');

    if (confirm('Use this title for the album? ' + title)) {
        $title.text(title);
        ajaxPost({
            cmd: 'update_album_title',
            title: title,
            albumid: $title.attr('albumid')
        });
    }
}

function copyCueTitle($this) {
    const title = getTitle($this);
    $('.make-cuesheet').val(title);
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
        $('.album-image').click(function () {
            $(this).toggleClass('expanded');
        });
        $('.cue-plus').click(function () {
            copyTitle($(this));
        });
        $('.cue-title').click(function() {
            copyCueTitle($(this));
        });
    }
});

