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
    ).keydown(function(e){
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
   $('.componist .remove').click(function(){
       removeComponist($(this));
   });
});

