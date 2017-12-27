/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    function prepareQuery() {
        // put query values in the hidden fields
        const types = ['componist', 'performer', 'tag', 'instrument'];
        types.forEach(function(type) {
            const $typeahead = $('.search .' + type + ' .typeahead.tt-input'),
                li = $typeahead.parents('li').first(),
                qq = li.find('.query');
            var val = '';
            if (qq.length === 0) {
                // console.log('Empty query for type ' + type);
                return;  // continue foreach: next type
            }
            $.each(qq, function(){
                const q = $(this);
                console.log('q', q.text());

                if (val.length) { val += ','; }
                val += getId(q.text());
            });
            console.log('val', val);
            $('.search input[name=' + type + ']').val(getId(val))
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

    function insertQueryElement($typeahead, val, input) {
        const
            clear =
            $('<span>')
                .text('x')
                .addClass('clear')
                .on('click', function(e){
                    const clear = $(e.target),
                        q2 = clear.prev('.query'),
                        li = q2.parent('li');
                    q2.remove();
                    clear.remove();
                }),
            q =
            $('<i>')
                .text(val)
                .addClass('query');

        q.insertAfter(input);
        clear.insertAfter(q);
        $typeahead.typeahead('val', '');
    }

    function impl_query_typeahead(items, type) {
        const $typeahead = $('.search .' + type + ' .typeahead'),
            li = $typeahead.parent('li'),
            input = li.find('input').last();
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).bind('typeahead:select', function(e, suggestion){
            insertQueryElement($typeahead, suggestion, input);
        })
            .keydown(function(e){
            if (e.key === 'Enter') {
                e.preventDefault();
            }
            if (e.key === 'Escape') {
                $typeahead.typeahead('val', '');
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

