$(function(){
    $('[href="#myGroup"]').click(function(){
        $('#all').addClass('in', 'active');
    });
});

$(function(){
    $('.group-delete').click(function(){
        var group_id = Number($(this).attr('victim'));
        var div = $(this).parent();
        console.log(group_id);
        $.getJSON($SCRIPT_ROOT + '/_delete_group',
            {group_id: group_id},
            function(data){
                if(data.success == '0'){
                    alert('failed!');
                }else{
                    $(div).remove();
                    alert('succeeded!');
                }
        });
    });
});
