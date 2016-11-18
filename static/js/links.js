/**
 * Created by Samuel on 11/7/2016
 */
$(function () {
    // variable declarations
    var obj = this; // give reference
    var $filesTable = $('#files-table');
    var $files = $('#files');
    var $information = $('#information');
    this.$selected = $(); // jquery equivalent null

    String.prototype.format = function (values) {
        var string = this;
        for (var key in values)
            if (values.hasOwnProperty(key)) {
                var regex = new RegExp("{" + key + "}", "g");
                string = string.replace(regex, values[key]);
            }

        return string;
    };

    window.fileElement = '<tr class="file">' +
        '<th class="user">{user}</th>' +
        '<th class="path">{path}</th>' +
        '<th class="url"><a href="{url}" target="_blank">{url}</a></th>' +
        '<th>{linkDate}</th>' +
        '<th>{age}</th>' +
        '</tr>';
    this.updateContents = function () {
        $.ajax({
            dataType: 'json',
            url: '/links',
            success: function(members) {
                $files.html('');
                members.forEach(function (member) {
                    console.log(member);
                    member.shared.forEach(function (file) {
                        var $fileElement = $(fileElement.format(obj.processFile(member.name, file))).data('file', obj.processFile(member.name, file));
                        $files.append($fileElement);
                    });
                });

                $filesTable.show(); // reveal files after load
                obj.fileListeners();
            }
        })
    };

    this.listeners = function () {

    };

    var emptyInfo = {
        'user': '',
        'path': '',
        'url': '',
        'linkDate': '',
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
    this.processFile = function (user, file) {
        var data = {};

        data.user = user;
        data.path = file.path;
        data.url = file.preview_url;
        data.linkDate = file.time_invited;
        data.age = file.days_old + ' days';

        return data;
    };


    this.updateInfo = function (info) {
        console.log('updated with', info);

        $('.user', $information).text(info.user);
        $('.path', $information).text(info.path);
        $('.url', $information).attr('href', info.url);
        $('.url', $information).text(info.url);
        $('.linkDate', $information).text(info.linkDate);
        $('.age', $information).text(info.age);
    };

    // run initial methods
    obj.updateContents();
    obj.listeners();
});