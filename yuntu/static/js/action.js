$(document).ready(function(){

    function send_clear_request() {
        var input;
        var arr;

        input = $("input[name='keyword']").val()
        arr = input.replace(/(^\s*)|(\s*$)/g, '').match(/[\u4E00-\u9FA5A-Za-z0-9 ]/g)
        if (arr == null) 
            keyword = ''
        else
            keyword = arr.join("").slice(0, 225)

        window.location.href="/show?keyword=" + keyword;
    }

    $("input[name='keyword']").keydown(function(e) {
        if (e.keyCode == 13) {
            send_clear_request()
        }
    })


    $('.btn').on('click', function(){
        send_clear_request()
    })
})

