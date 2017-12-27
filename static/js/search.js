/**
 * Created by orion on 14/11/2017.
 */

'use strict';

$(function () {
    function prepareQuery() {
        const types = ['componist', 'performer', 'tag', 'instrument'];
        types.forEach(function(type) {
            var $typeahead = $('.upload-controls .' + type + ' .typeahead.tt-input');
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

    // function query() {
    //     var q = '';
    //     const qComponist = $('.search .componist .typeahead.tt-input').val(),
    //         qTag = $('.search .tag .typeahead.tt-input').val(),
    //         qPerformer = $('.search .performer .typeahead.tt-input').val(),
    //         qInstrument = $('.search .instrument .typeahead.tt-input').val();
    //     console.log(qComponist);
    //     if (qComponist.length) {
    //         q = 'componist=' + getId(qComponist);
    //     }
    //     if (qPerformer.length) {
    //         if (q.length) { q += '&';}
    //         q += 'performer=' + getId(qPerformer);
    //     }
    //     if (qTag.length) {
    //         if (q.length) { q += '&';}
    //         q += 'tag=' + getId(qTag);
    //     }
    //     if (qInstrument.length) {
    //         if (q.length) { q += '&';}
    //         q += 'instrument=' + getId(qInstrument);
    //     }
    //     if (q.length) { q = '?' + q;}
    //     // console.log(q);
    //     document.location.href = '/search' + q;
    // }

    function impl_query_typeahead(items, type) {
        const $typeahead = $('.search-controls .' + type + ' .typeahead'),
            li = $typeahead.parent('li'),
            span = li.find('input').last();
        const $realtypeahead = $('.search-controls .' + type + ' .typeahead.tt-input');
        $typeahead.typeahead(typeaheadSettings,
            { source: match(items) }
        ).keydown(function(e){
            if (e.key === 'Enter') {
                console.log(span);
                $('<i>')
                    .text($typeahead.val())
                    .insertAfter(span);
                $typeahead.val('');
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
        // $('.do-search').click(function() {
        //     query();
        // });
        $('.search input[type=submit]').click(function() {
            prepareQuery();
            return true;
        });
        $('.search .clear').click(function(){
            clearSearch($(this));
        });
    }});

