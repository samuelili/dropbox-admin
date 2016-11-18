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
        '<th class="path">{path}</th>' +
        '<th class="url"><a href="{url}" target="_blank">{url}</a></th>' +
        '<th>{linkDate}</th>' +
        '<th>{expiration}</th>' +
        '</tr>';
    this.updateContents = function () {
        $.ajax({
            dataType: 'json',
            url: '/links',
            success: function (files) {
                console.log('Retrieved', files);
                $files.html(''); // clean

                files.forEach(function (file) {
                    var $fileElement = $(fileElement.format(obj.processFile(file))).data('file', obj.processFile(file));

                    $files.append($fileElement);
                });

                $filesTable.show(); // reveal files after load
                obj.fileListeners();
            }
        })
    };

    this.listeners = function () {

    };

    var emptyInfo = {
        'path': '',
        'url': '',
        'linkDate': '',
        'expiration': ''
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
    this.processFile = function (file) {
        var data = {};

        data.path = file._path_lower_value;

        data.url = 'No Url';
        if (file._url_present)
            data.url = file._url_value.substring(0, file._url_value.length - 5);

        data.linkDate = 'None';

        data.expiration = 'None';
        if (file._expires_value != null)
            file.expiration = file._expires_value;

        return data;
    };

    this.updateInfo = function (info) {
        console.log('updated with', info);

        $('.path', $information).text(info.path);
        $('.url', $information).attr('href', info.url);
        $('.url', $information).text(info.url);
        $('.linkDate', $information).text(info.linkDate);
        $('.expiration', $information).text(info.expiration);
    };

    // run initial methods
    obj.updateContents();
    obj.listeners();
});