$(function(){
    $('.discuss-delete').click(function(){
        var discuss_id = Number($(this).attr('victim'));
        var div = $(this).parent();
        console.log(discuss_id);
        $.getJSON($SCRIPT_ROOT + '/_delete_discussion',
            {discuss_id: discuss_id},
            function(data){
                if(data.success == '0'){
                    alert('failed');
                }else{
                    $(div).remove();
                    alert('succeeded!');
                }
        });
    });
});
