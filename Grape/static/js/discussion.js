$(function(){
    $('#reply-form').submit(function(e){
        e.preventDefault();
        var content = $('#reply-content').val();
        var url = window.location.href;
        var patt = /dis+[0-9]*/g;
        url = url.match(patt)[1];
        patt = /[^0-9]/g;
        var dis_id = url.replace(patt, '');
        if(content == ''){
            alert('please enter something!');
        }else {
            $.getJSON($SCRIPT_ROOT + '/_reply_discussion/' + dis_id,
                {content: content},
                function (data) {
                    if (data.status == 'success') {
                        location.reload();
                    }else{
                        alert(data.status);
                    }
                });
        }
    });
});



$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.reply-delete').click(function(){
            var reply_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(reply_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_reply',
                {reply_id: reply_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        alert('succeeded!');
                        location.reload();
                    }
            });
        });
    });
});