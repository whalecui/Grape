//set anchor
$(function(){
    $('.tab-main').click(function(){
        location.hash = $(this).attr('href');
    });
});

$(function(){
    var anchor = location.hash;
    console.log(anchor);
    $('div.tab-group ul li a[href="'+anchor+'"]').tab('show');
});
