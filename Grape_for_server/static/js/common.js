//set anchor
$(function(){
    $('.tab-main').click(function(){
        location.hash = $(this).attr('href');
    });
});

$(function(){
    var anchor = location.hash;
    $('div.tab-group ul li a[href="'+anchor+'"]').tab('show');
});

//detail.js
$(function(){
    $('.show-detail').click(function(){
        var target = $($(this).attr('data-target'));
        $(target).animate(
            {height:'toggle'}
        );
    });
});

$(function(){
    $(".popover-options").popover({html : true });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.popover-close').click(function(){
            $($(this).attr('origin')).popover('hide');
        });
    });
});
