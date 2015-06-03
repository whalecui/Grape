$(function(){
    $('#reply-form').submit(function(e){
        e.preventDefault();
        var content = $('#reply_content').val();
        if(content == ''){
            alert('please enter something!');
        }else {
            $.getJSON($SCRIPT_ROOT + '/_login',
                {content: content},
                function (data) {
                    alert(data.status);
                    if (data.status == 'success') {
                        location.reload();
                    }
                });
        }
    });
});
