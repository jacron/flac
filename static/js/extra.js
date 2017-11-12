/**
 * Created by orion on 28/10/2017.
 */
$(function () {
    $('.input-album').keydown(function(e){
        if (e.key === 'Enter') {
            var target = $(e.target).val();
            location.href="/album/" + target;
        }
    });
    $('.delete-album').keydown(function(e){
        if (e.key === 'Enter') {
            var target = $(e.target).val();
            if (confirm('album ' + target + ' verwijderen?')){
                const data = {
                    cmd: 'delete_album',
                    albumid: target
                };
                ajaxPost(data);
            }
        }
    });
    $('.extra .add-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            var $target = $('.componisten input.add');
            addNewComponist($target);
        }
    });
});
