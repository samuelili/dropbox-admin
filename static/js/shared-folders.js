/**
 * Created by Samuel on 11/7/2016
 */
$(function () {
    // variable declarations
    var obj = this; // give reference
    var $filesTable = $('#files-table');
    var $files = $('#files');
    var $information = $('#information');
    var $loading = $('#loading-screen');
    this.$selected = $(); // jquery equivalent null

    window.fileElement = '<tr class="file">' +
        '<th class="user"><a href="/pages/dashboard?name={user}&member-id={memberId}">{user}</a></th>' +
        '<th class="path"><a href="{url}">{path}</a></th>' +
        '<th class="access">{access}</th>' +
        '<th class="age" style="color: {ageColor}">{age}</th>' +
        '</tr>';
    this.updateContents = function (forceUpdate) {
        $filesTable.hide();
        $loading.show();
        $.ajax({
            dataType: 'json',
            url: '/shared-folders?force-update=' + (forceUpdate ? '1' : '0'),
            success: function (members) {
                $files.html('');
                console.log('Retrieved', members);
                members.forEach(function (member) {
                    /** @namespace member.shared */
                    member.shared.forEach(function (share) {
                        var $fileElement = $(fileElement.format(obj.processFile(member, share))).data('file', obj.processFile(member, share));
                        $files.append($fileElement);
                    });
                });

                $loading.hide();
                $filesTable.show(); // reveal files after load
                obj.fileListeners();
            }
        })
    };

    this.listeners = function () {
        $('#force-refresh').on('click', function () {
            obj.updateContents(true);
        });
    };

    var emptyInfo = {
        'user': '',
        'path': '',
        'access': '',
        'url': '',
        'linkDate': '',
        'memberId': '',
        'age': ''
    };
    this.fileListeners = function () {
        $('.file', $files).on('click', function () {
            obj.$selected.removeClass('active');
            obj.updateInfo(emptyInfo);
            if (obj.$selected[0] != this) {
                $(this).toggleClass('active');
                obj.updateInfo($(this).data('file'));
            }

            obj.$selected = $(this);
        });
    };

    // requires path, url, link date, expiration
    this.processFile = function (member, file) {
        var data = {};

        data.user = member.display_name;
        data.memberId = member.team_member_id;
        data.path = file.path;
        data.access = file.access_type;
        data.url = file.preview_url;
        data.linkDate = file.time_invited;

        data.age = file.days_old;
        data.ageColor = 'ForestGreen';
        if (data.age >= 180)
            data.ageColor = 'Crimson';
        else if (data.age >= 90)
            data.ageColor = 'Coral';

        return data;
    };


    this.updateInfo = function (info) {
        console.log('updated with', info);

        $('.user', $information).text(info.user);
        $('.memberId', $information).text(info.memberId);
        $('.path', $information).text(info.path);
        $('.access', $information).text(info.access);
        $('.url', $information).attr('href', info.url);
        $('.url', $information).text(info.url);
        $('.linkDate', $information).text(info.linkDate);
        $('.age', $information).text(info.age);
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