/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    function prepareQuery() {
        const types = ['componist', 'performer', 'tag', 'instrument'];
        types.forEach(function(type) {
            var $typeahead = $('.search .' + type + ' .typeahead.tt-input');
            $('.search input[name=' + type + ']').val(getId($typeahead.val()))
        });
    }

    function getId(s) {
        var pos = s.lastIndexOf('_');
        return s.substr(pos + 1);
    }

    function clearSearch($this) {
        const $li = $this.parent('li').first();
        $li.find('.typeahead.tt-input').val('');
    }

    function impl_query_typeahead(items, type) {
        const $typeahead = $('.search .' + type + ' .typeahead'),
            li = $typeahead.parent('li'),
            span = li.find('input').last();
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).keydown(function(e){
            if (e.key === 'Enter') {
                console.log(span);
                $('<i>')
                    .text($typeahead.val())
                    .insertAfter(span);
                // $typeahead.val('');
            }
            if (e.key === 'Escape') {
                $typeahead.val('');
            }
        });
    }

    function typeAheadSearch(cmdGet, nameField, type) {
        ajaxGet({
            cmd: cmdGet
        }, function(response){
            var items = [];
            response.forEach(function(item) {
                items.push(item[nameField] + '_' + item.ID);
            });
            impl_query_typeahead(items, type);
        });
    }

    if ($('.search').length) {
        // functions for the search page
        typeAheadSearch('instruments', 'Name', 'instrument');
        typeAheadSearch('performers', 'FullName', 'performer');
        typeAheadSearch('componisten', 'FullName', 'componist');
        typeAheadSearch('tags', 'Name', 'tag');
        $('.search input[type=submit]').click(function() {
            prepareQuery();
            return true;
        });
        $('.search .clear').click(function(){
            clearSearch($(this));
        });
    }});

