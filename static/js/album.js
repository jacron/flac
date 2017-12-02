/**
 * Created by orion on 22/10/2017.
 */
'use strict';


$(function () {
    function getTitle($this) {
        const parent = $this.parents('.cue-header').find('span').first();
        return parent.text();
    }
    function editAlbumTitle($this, albumId) {
        ajaxPost({
            cmd: 'update_album_title',
            title: $this.text(),
            albumid: albumId
        })
    }
    function copyTitle($this, albumId) {
        const title = getTitle($this),
            $title = $('.edit-title');

        if (confirm('Use this title for the album? ' + title)) {
            $title.text(title);
            ajaxPost({
                cmd: 'update_album_title',
                title: title,
                albumid: albumId
            });
        }
    }
    function copyCueTitle($this) {
        const title = getTitle($this);
        $('.make-cuesheet').val(title);
    }
    function editCuesheet($this, albumid) {
        ajaxPost({
            cmd: 'editcuesheet',
            id: $this.attr('id'),
            albumid: albumid
        })
    }
    function splitCuedFile($this, albumid) {
        ajaxPost({
            cmd: 'split_cued_file',
            cue_id: $this.attr('id'),
            albumid: albumid
        }, function(response) {
           // console.log(response)
        });
    }
    function cycleSizes($this) {
        if ($this.hasClass('expanded')) {
            $this.removeClass('expanded');
            $this.addClass('super');
        }
        else if ($this.hasClass('super')) {
            $this.removeClass('super');
        }
        else {
            $this.addClass('expanded');
        }
    }
    function combineCuesheets(albumId) {
        ajaxPost({
            cmd: 'combinesubs',
            albumid: albumId
        }, function() {
            refetch();
        });
    }
    function makeSubs(albumId) {
        ajaxPost({
            cmd: 'makesubs',
            albumid: albumId
        }, function() {
            refetch();
        });
    }
    function normCuesheet($this, albumid) {
        ajaxPost({
            cmd: 'normcuesheet',
            albumid: albumid,
            id: $this.attr('id')
        }, function()  {
            refetch();
        });
    }
    function removeAlbum(albumId, idText) {
        if (confirm('Album ' + albumId + ' verwijderen?')) {
            ajaxPost({
                cmd: 'delete_album',
                album_id: albumId
            }, function() {
                idText.hide();
            });
        }
    }
    function adjustKk(album_id, $this) {
        ajaxPost({
            cmd: 'adjust_kk',
            albumid: album_id
        }, function(){
            $this.hide();
        });
    }
    function inheritElements(albumId) {
        ajaxPost({
            cmd: 'inherit_elements',
            albumid: albumId
        }, function(response) {

        });
    }
    function filterAlbums($input) {
        var search = $input.val().toLowerCase();
        $('.album-list li').each(function() {
            var li = $(this),
                title = li.find('.title'),
                text = title.text().toLowerCase();
            if (!search.length || text.indexOf($input.val()) !== -1) {
                li.show();
            } else {
                li.hide();
            }
        });
    }

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
            cycleSizes($(this));
        });
        $('.cue-plus').click(function () {
            copyTitle($(this), albumId);
        });
        $('.cue-title').click(function() {
            copyCueTitle($(this));
        });
        $('.cue-split').click(function() {
            splitCuedFile($(this), albumId);
        });
        $('.cue-edit').click(function() {
            editCuesheet($(this), albumId);
        });
        $('.cue-norm').click(function() {
            normCuesheet($(this), albumId);
        });
        $('.make-subs').click(function() {
            makeSubs(albumId);
        });
        $('.combine-subs').click(function() {
            combineCuesheets(albumId);
        });
        $('.album .ID .remove').click(function() {
            removeAlbum(albumId, $('.album .ID'));
        });
        $('.kk').click(function() {
            adjustKk(albumId, $(this));
        });
        $('.inherit-elements').click(function(){
            inheritElements(albumId);
        });
    }
    // albumlist also lives on componist page etc
    $('.filter-albums').keydown(function(e){
        if (e.key === 'Enter') {
            filterAlbums($(this));
        }
    })

});

