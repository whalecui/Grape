
$(function(){
    $('[href="#myGroup"]').click(function(){
        $('#all').addClass('in', 'active');
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.group-delete').click(function(){
            var group_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(group_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_group',
                {group_id: group_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        //$(div).remove();
                        //alert('succeeded!');
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.group-quit').click(function(){
            var group_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(group_id);
            $.getJSON($SCRIPT_ROOT + '/_quit_group',
                {group_id: group_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        //$(div).remove();
                        //alert('succeeded!');
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.group-delete-admin').click(function(){
            var group_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(group_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_group_admin',
                {group_id: group_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.user-delete').click(function(){
            var user_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(user_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_user',
                {user_id: user_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});



$(function(){
    $('#create-group').submit(function(e){
        var error = '<i class="fa fa-times"></i>';
        var flag = true;
        e.preventDefault();
        var name = $('#group-name').val();
        var topic = $('#group-topic').val();
        var desc = $('#group-desc').val();
        var confirm = $('#group-confirm').val();
        if(name == ''){
            flag = false;
            var tmp = $('#group-name').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
            $('#group-name').before(error);
        }else{
            var tmp = $('#group-name').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
        }
        if(topic == ''){
            flag = false;
            var tmp = $('#group-topic').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
            $('#group-topic').before(error);
        }else{
            var tmp = $('#group-topic').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
        }
        if(confirm == ''){
            flag = false;
            var tmp = $('#group-confirm').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
            $('#group-confirm').before(error);
        }else{
            var tmp = $('#group-confirm').parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
        }
        if(flag){
            $.getJSON($SCRIPT_ROOT + '/_new_group',
                {name: name, topic: topic, desc: desc, confirm: confirm},
                function(data){
                    if(data.status == 'exist'){
                        alert('This group name is already used!');
                        var tmp = $('#group-name').parent().find('i')[0];
                        if(tmp){ $(tmp).remove(); }
                        $('#group-name').before(error);
                    }else if(data.status == 'success'){
                        location.reload();
                    }else{
                        alert('please input valid ' + data.status);
                    }
            });
        }
    });
});


$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.message_confirm').click(function(){
            var user_id = Number($(this).attr('victim1'));
            var message_id = Number($(this).attr('victim2'));
            var div = $(this).parent();
            console.log(user_id);
            $.getJSON($SCRIPT_ROOT + '/_message_confirm',
                {user_id: user_id, message_id: message_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});
