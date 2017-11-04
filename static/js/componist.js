/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addComponist($select) {
    const data = {
        cmd: 'add_componist',
        componistid: $select.val(),
        albumid: $select.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function newComponist($input) {
    const data = {
        cmd: 'new_componist',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function addNewComponist($input) {
    const data = {
        cmd: 'abs_new_componist',
        name: $input.val()
    };
    ajaxPost(data, function (id) {
        console.log(id);
        $('.componist-added').text(id);
    });
    // location.reload();
}

function removeComponist($this) {
    const data = {
        cmd: 'remove_componist',
        id: $this.attr('id'),
        albumid: $this.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

var match = function (items) {
    return function findMatches(q, cb) {
        var matches, substrRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(items, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });

        cb(matches);
    };
};

$(function () {
    var componisten = [];
    $('.componist-naam').each(function () {
        var $this = $(this);
        componisten.push($this.text());
    });
    $('.componisten .add').keydown(function (e) {
        if (e.key === 'Enter') {
            var $target = $('.componisten input.add');
            // console.log($target);
            addNewComponist($target);
        }
    });
    $('.componisten .typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 1,
            display: 'name'
        },
        {
            name: 'componisten',
            source: match(componisten)
        }
    ).keydown(function (e) {
        if (e.key === 'Enter') {
            var result = $('.typeahead').get(1).value;
            $('.componist-naam').each(function () {
                var $this = $(this);
                if ($this.text() === result) {
                    location.href = '/componist/' + $this.attr('componistid');
                }
            });
        }
    });
});

function editComponistName($this) {
    const data = {
        cmd: 'update_componist_name',
        name: $this.text().trim(),
        id: $this.attr('componist_id')
    };
    ajaxPost(data);
}

function editComponistYears($this) {
    const data = {
        cmd: 'update_componist_years',
        years: $this.text().trim(),
        id: $this.attr('componist_id')
    };
    ajaxPost(data);
}

function preventSpilledDrop(obj) {
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        obj.css('border', '2px dotted #0B85A1');
    });
    obj.on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
}

function uploadFile(fd, obj) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        url: url,
        data: fd,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        headers: headers,
        success: function(msg){
            console.log(msg);
            obj.css('border', 'none');
            location.reload();
        },
        failure: function(msg){
            console.log(msg);
            obj.css('border', 'none');
        }
    });
}

function handleFileUpload(files, obj, personId, fieldName) {
    for (var i = 0; i < files.length; i++) {
        const file = files[i];
        console.log(file);
        var fd = new FormData();
        fd.append('file', file);
        fd.append('cmd', 'upload');
        fd.append(fieldName, personId)
        uploadFile(fd, obj);
    }
}

function handleDrop(obj, personId, fieldName) {
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function (e) {
        $(this).css('border', '2px dotted #0B85A1');
        e.preventDefault();
        var files = e.originalEvent.dataTransfer.files;
        console.log(files);

        //We need to send dropped files to Server
        handleFileUpload(files, obj, personId, fieldName);
    });
}

$(function () {
    // componist
    $('.edit-componist-name').keydown(function (e) {
        if (e.key === 'Tab') {
            editComponistName($(this));
        }
    });
    $('.edit-componist-years').keydown(function (e) {
        if (e.key === 'Tab') {
            editComponistYears($(this));
        }
    });
    $('button.select-componist').click(function () {
        addComponist($('select.select-componist'));
    });
    $('button.add-componist').click(function () {
        newComponist($('input.add-componist'));
    });
    $('input.add-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            newComponist($('input.add-componist'));
        }
    });
    $('select.select-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            addComponist($('select.select-componist'));
        }
    });
    $('.componist .remove').click(function () {
        removeComponist($(this));
    });
    $('.add-componist').click(function (e) {
        var $target = $(e.target),
            id = $target.attr('id'),
            albumId = $('#album_id').val();
        // console.log(id, albumId);
        const data = {
            cmd: 'add_componist',
            componistid: id,
            albumid: albumId
        };
        ajaxPost(data);
        location.reload();
    });
    const componist_id = $('#componist_id').val();
    handleDrop($('#drop-area-componist'), componist_id, 'componist_id');
    preventSpilledDrop($('.componist'));
});

