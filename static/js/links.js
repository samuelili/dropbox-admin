/**
 * Created by Samuel on 11/7/2016
 */
$(function () {
    // variable declarations
    var obj = this; // give reference
    var $filesTable = $('#files-table');
    var $links = $('#links');
    var $information = $('#information');
    var $loading = $('#loading-screen');
    this.$selected = $(); // jquery equivalent null

    var linkHtml = '<tr class="file">' +
        '<th><a href="/pages/dashboard?name={member}&member-id={memberId}">{member}</a></th>' +
        '<th>{name}</th>' +
        '<th>{expiration}</th>' +
        '<th><a href="{url}" target="_blank">{path}</a></th>' +
        '<th>{visible}</th></tr>';
    this.updateContents = function (forceUpdate) {
        $filesTable.hide();
        $loading.show();

        $.ajax({
            dataType: 'json',
            url: '/links?force-update=' + (forceUpdate ? '1' : '0'),
            success: function (members) {
                $links.html('');
                console.log('Retrieved', members);

                members.forEach(function (member) {
                    member.links.forEach(function (link) {
                        var $linkElement = $(linkHtml.format(obj.processLink(member, link))).data('link', obj.processLink(member, link));
                        $links.append($linkElement);
                    });
                });
                $loading.hide();
                $filesTable.show(); // reveal files after load

                obj.linkListeners();
            }
        })
    };

    this.listeners = function () {
        $('#force-refresh').on('click', function () {
            obj.updateContents(true);
        });
    };

    var emptyInfo = {
        'expiration': '',
        'member': '',
        'memberId': '',
        'path': '',
        'url': '',
        'user': ''
    };
    this.linkListeners = function () {
        $('.file', $links).on('click', function () {
            obj.$selected.removeClass('active');
            obj.updateInfo(emptyInfo);
            if (obj.$selected[0] != this) {
                $(this).toggleClass('active');
                obj.updateInfo($(this).data('link'));
            }

            obj.$selected = $(this);
        });
    };

    this.processLink = function (member, link) {
        var data = {};

        data.member = member.display_name;

        data.revoke = link.can_revoke;
        data.revokeColor = 'ForestGreen';
        if (!data.revoke)
            data.revokeColor = 'Crimson';

        data.name = link.name;
        data.path = link.path;
        data.url = link.url;

        data.expiration = link.expires;
        if (link.expires == null)
            data.expiration = 'Never';

        data.visible = link.visibility;
        data.memberId = member.team_member_id;

        return data;
    };


    this.updateInfo = function (info) {
        console.log('Updated with', info);

        $('.member', $information).text(info.member);
        $('.revoke', $information).text(info.revoke);
        $('.name', $information).text(info.name);
        $('.path', $information).text(info.path);
        $('.expiration', $information).text(info.expiration);
        $('.member_id', $information).text(info.memberId);
        $('.url').attr('href', info.url);
        $('.url', $information).text(info.url);

    };

    // run initial methods
    if (!$loading[0].complete)
        $('#loading-gear', $loading).on('load', function () {
            obj.updateContents(false);
        });
    else
        obj.updateContents(false);
    obj.listeners();
});