/**
 * Created by samuel on 11/19/16.
 */

$(function () {
    var obj = this;
    this.teamMemberId = window.location.hash.substr(1);
    var $shared = $('#shared-table');
    var $links = $('#links-table');

    obj.updateContents = function () {
        if (obj.teamMemberId != "") {
            console.log('id', obj.teamMemberId);
            $('#team-member-id').text(obj.teamMemberId);

            // get shared
            $.ajax({
                'url': '/members/{teamMemberId}/shared-folders'.format({
                    teamMemberId: obj.teamMemberId
                }),
                'method': 'GET',
                'dataType': 'json',
                success: function (shared) {
                    console.log('Retreieved Shared', shared);

                    obj.displayShared(shared);
                }
            });

            // get links
            $.ajax({
                'url': '/members/{teamMemberId}/shared-links'.format({
                    teamMemberId: obj.teamMemberId
                }),
                'method': 'GET',
                'dataType': 'json',
                success: function (links) {
                    console.log('Retreieved Links', links);

                    obj.displayLinks(links);
                }
            });
        } else {
            $('#no-id-modal').modal();
        }
    };

    var shareHtml = '<tr>' +
        '<th>{access}</th>' +
        '<th>{name}</th>' +
        '<th><a href="{url}" target="_blank">{path}</a></th>' +
        '<th style="color: {daysColor}">{days}</th>' +
        '<th>{invited}</th>' +
        '<th>{sharedFolderId}</th></tr>';
    this.displayShared = function (shared) {
        $shared.html(''); // clean

        shared.forEach(function (share) {
            var $shareElement = $(shareHtml.format(obj.processShared(share)));

            $shared.append($shareElement);
        });
    };

    this.processShared = function (share) {
        var data = {};

        data.access = share.access_type;
        data.name = share.name;
        data.url = share.preview_url;
        data.path = share.path;

        data.days = share.days_old;
        data.daysColor = 'ForestGreen';
        if (data.days >= 180)
            data.daysColor = 'Crimson';
        else if (data.days >= 90)
            data.daysColor = 'Coral';

        data.invited = share.time_invited;
        data.sharedFolderId = share.shared_folder_id;

        return data;
    };

    var linksElement = '<tr>' +
        '<th style="color: {revokeColor}">{revoke}</th>' +
        '<th>{name}</th>' +
        '<th>{expiration}</th>' +
        '<th><a href="{url}" target="_blank">{path}</a></th>' +
        '<th>{visible}</th></tr>';
    this.displayLinks = function (links) {
        $links.html(''); // clean

        links.forEach(function(link) {
            var $linkElement = $(linksElement.format(obj.processLink(link)));

            $links.append($linkElement);
        });
    };

    this.processLink = function(link) {
        var data = {};

        data.revoke = link.can_revoke? 'Yes': 'No';
        data.revokeColor = 'ForestGreen';
        if (!link.can_revoke)
            data.revokeColor = 'Crimson';

        data.name = link.name;
        data.path = link.path;
        data.url = link.url;

        data.expiration = link.expires;
        if (link.expires == null)
            data.expiration = 'Never';

        data.visible = link.visibility;

        return data;
    };

    obj.updateContents();
});