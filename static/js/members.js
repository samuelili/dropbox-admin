/**
 * Created by samuel on 11/19/16.
 */
$(function () {
    var obj = this;
    var $membersTable = $('#members-table');
    this.$selected = $();

    var memberHtml = '<tr>' +
        '<th>' +
        '<a class="btn btn-primary btn-xs edit-button" href="/pages/dashboard?name={name}&member-id={id}">' +
        '<span class="glyphicon glyphicon-pencil"></span> Edit' +
        '</a></th>' +
        '<th>{name}</th>' +
        '</tr>';
    obj.updateContents = function () {
        $.ajax({
            dataType: 'json',
            url: '/members',
            success: function (members) {
                $membersTable.html(''); // clean
                console.log('Retrieved', members);

                members.forEach(function (member) {
                    var $memberRow = $(memberHtml.format({
                        "name": member.display_name,
                        "id": member.team_member_id
                    }));
                    $membersTable.append($memberRow);
                });

                obj.memberListeners();
            }
        })
    };

    this.memberListeners = function () {
        $('tr', $membersTable).hover(function () {
            $(this).find('.edit-button').show();
        }, function () {
            $(this).find('.edit-button').hide();
        });
    };

    obj.updateContents();
});