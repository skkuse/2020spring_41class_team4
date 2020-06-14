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

var pname = document.getElementById('pname').innerHTML;
var div = document.getElementById('recommend_item');
// 추천 알고리즘
$.ajax({
    url:'/recommend/item/',
    method:'POST',
    dataType:'json',
    data:{
        'item': pname,
        'other':'false'
          },
    success:function(recommend_data) {
        for(var j = 0; j < 3; j++){  // 3개만
            div.innerHTML += '<div style= " float: left; padding: 10px; width: 33%;" class="card_inner">\
                                    <div class="card_top">\
                                        <img src=' + recommend_data[j].book_img + ' style="display:block;margin:0px auto;width:190px; height:230px;">\
                                    </div>\
                                    <div class="card_bottom">\
                                        <div class="card_info">\
                                        <p style="font-size:16px;text-align:center;">' + recommend_data[j].bk + '</p>\
                                    </div>\
                                    </div>';
        }      
    },
    error:function(err) {
        console.log('추천 정보가 없습니다!');
        var li = document.createElement('li');
        li.innerText = "추천 정보가 없습니다!";
        div.appendChild(li);
    }
});