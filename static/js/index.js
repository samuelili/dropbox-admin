/**
 * Created by Samuel on 11/7/2016
 */
$(function () {
    // variable declarations
    var obj = this; // give reference
    var $delete = $('#delete');
    var $filesTable = $('#files-table');
    var $files = $('#files');
    this.$selected = $();

    String.prototype.format = function (values) {
        var string = this;
        for (var key in values)
            if (values.hasOwnProperty(key)) {
                var regex = new RegExp("{" + key + "}", "g");
                string = string.replace(regex, values[key]);
            }

        return string;
    };

    // http://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript
    this.formatBytes = function (bytes, decimals) {
        if (bytes == 0) return '0 Byte';
        var k = 1024;
        var dm = decimals + 1 || 3;
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        var i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    };

    window.fileElement = '<tr class="file"><th class="icon" scope="row">{icon}</th><td class="file-name">{name}</td><td>{type}</td><td>{size}</td></tr>';
    var extensionRegex = /(?:\.([^.]+))?$/;
    this.updateContents = function () {
        $.ajax({
            dataType: 'json',
            url: '/crud/read',
            success: function (files) {
                console.log('Retrieved', files);
                $files.html(''); // clean

                files.forEach(function (file) {
                    var $fileElement = $(fileElement.format({
                        name: file.name.replace(/\.[^/.]+$/, ""),
                        type: (function () {
                            var extension = extensionRegex.exec(file.name)[1];
                            if (extension != undefined)
                                return extension;
                            return 'none';
                        }),
                        size: obj.formatBytes(file.size),
                        icon: 'insert_drive_file'
                    })).data('filename', file.name);

                    $files.append($fileElement);
                });

                $filesTable.show(); // reveal files after load
                obj.fileListeners();
            }
        })
    };

    this.listeners = function() {
        $delete.on('click', function() {
            if (!$delete.hasClass('disabled')) {
                $.ajax({
                    method: 'DELETE',
                    url: '/crud/delete',
                    headers: {
                        'filename': obj.$selected.data('filename')
                    },
                    success: function() {
                        obj.updateContents();
                    }
                });
            }
        });
    };


    this.fileListeners = function () {
        $('.file', $files).on('click', function () {
            obj.$selected.removeClass('active');
            $delete.removeClass('disabled');
            if (obj.$selected[0] != this)
                $(this).toggleClass('active');
            else // if deselecting
                $delete.addClass('disabled');

            obj.$selected = $(this);
        });
    };

    // run initial methods
    obj.updateContents();
    obj.listeners();
});