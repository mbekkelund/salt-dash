$().ready(function(){

    $("#filter").keyup(function(){
        var filter = $(this).val(), count = 0;
        $(".filtered:first tr").each(function(){
            if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                $(this).addClass("filtered-hidden");
            }
            else {
                $(this).removeClass("filtered-hidden");
                count++;
            }
        });
        $("#filter-count").text(count);
    });
    
    
    
    $('a.toggle').click(function() {
        var id = $(this).attr('data:toggle');
        $(this).toggleClass('off');
        
        if($(this).hasClass('off')) {
            $('#' + id).fadeOut(100);
        } else {
            $('#' + id).fadeIn(100);
        }
        
    })
})


