$('#btn_board_new').on('click', function() {
    window.location.replace("/post/register");
});

$('#btn_board_list').on('click', function() {
    window.location.replace("/post/");
});

$('#btn_board_buy').on('click',function(){
    $.ajax({
        url:'/board/update',
        method:'PUT',
        dataType:'json',
        data:'',
        success:function(data){
            if(data.status =='OK'){
                data.board_status = "1"
                var elem = document.getElementById("board_status");
                elem.value == "거래중";
                alert('구매신청 완료!')
                //구매 게시글 status 상태 변경해야함
            }else{
                alert('구매신청 실패!')
            }
        }
    })
})
function btn_board_status()
{
    var elem = document.getElementById("board_status");
    if (elem.value=="판매중") elem.value = "판매완료";
    else elem.value = "판매중";
}

$('#btn_board_update').on('click', function() {
    $.ajax({
        url:'/board/update',
        method:'PUT',
        dataType:'json',
        contentType:'application/json',
        data:JSON.stringify({
            'bid':$('#bid').val(),
            'board_title':$('#board_title').val(),
                             'board_content':$('#board_content').val(),
                             'board_seller_name':$('#board_seller_name').val(),
                             'board_seller_tel':$('#board_seller_tel').val()
                            }),
        success:function(data) {
            if(data.status == 'OK') {
                alert('업데이트에 성공!');
                window.location.replace('/board/list');
            } else {
                alert('업데이트에 실패!, 다시 시도!1');    
            }
        },
        error:function(err) {
            alert('업데이트에 실패!, 다시 시도!2');
        }
    });
});

$('#btn_board_delete').on('click', function() {
    $.ajax({
        url:'/board/update',
        method:'DELETE',
        dataType:'json',
        contentType:'application/json',
        data:JSON.stringify({'bid':$('#bid').val()}),
        success:function(data) {
            if(data.status == 'OK') {
                alert('삭제 성공!');
                window.location.replace('/board/list');
            } else {
                alert('삭제 실패!, 다시 시도!1');    
            }
        },
        error:function(err) {
            alert('삭제 실패!, 다시 시도!2');
        }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function showPopup() { window.open("pop_up", "a", "width=400, height=300, left=100, top=50"); }

$('#btn_logout').on('click', function() {
    window.location.replace("/email_auth/logout/");
});

function get_locker_list(){
    $.ajax({
        url:'/rest/lockers/',
        method:'GET',
        dataType:'json',
        success:function(data){

            var table = document.getElementById('title_locker');

            for (var i = 0; i < data.length; i++) {
    
                var tr = document.createElement('tr');
                var locker_id = data[i].id;
                var locker_number = data[i].number;
                var locker_status = data[i].status;
                var locker_location = data[i].location;
    
               
    
               tr.innerHTML = "<td width='20%' align='center'>" + locker_number + "</td><td width='20%' align='center'>" + locker_status + "</td>" + locker_status + "<td width='40%' align='center'></td>" + locker_location+ "<td width='20%' align='center'><input type='radio' name='locker_status_check'></td>"
               table.appendChild(tr);
            
            }
   
        }
    })
}

// post list
// $(document).ready(function(){
    
    
 
// });
 
