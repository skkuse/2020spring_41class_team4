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

var search_input = document.querySelector("#search_input");
var table_body = document.querySelector(".table_body ul");
var status_list = ["판매중", "판매완료"];
var status_style_list = ["open", "closed"];

$.ajax({
    url:'/rest/posts/',
    method:'GET',
    dataType:'json',
    contentType:'application/json',
    success:function(data) {

        for (var i = 0; i < data.length; i++) {

            var li = document.createElement('li');
      var id = data[i].id;
      var title = data[i].title;
      var user_id = data[i].user_id;
      var status = status_list[data[i].status];
      var status_style = status_style_list[data[i].status];
      var locker = data[i].locker_check;
      if (locker == 0) locker = "";
      var uname = "";
      var pN = null;

      $.ajax({
        url:'/rest/users/' + user_id + '/',
        method:'GET',
        dataType:'json',
        async: false,
        contentType:'application/json',
        success:function(udata) {
          uname = udata.uname;
          pN = udata.phone_number;
        }
      });

      li.innerHTML = "\
      <div class='item'>\
      <div class='name'>\
        <span>" + uname + "</span>\
      </div>\
      <div class='phone'>\
        <span>" + pN + "</span>\
      </div>\
      <div class='issue'>\
        <span><a href=/home/product/" + id + "/>"  + title + "</a></span>\
      </div>\
      <div class='locker'>\
        <span>" + locker + "</span>\
      </div>\
      <div class='status'>\
        <span class='" + status_style + "'>" + status + "</span>\
      </div>\
      </div>";
      table_body.appendChild(li);
        
        }

    },
    error:function(err) {
        alert('실패2');
    }
});

$('#search_btn').on('click', function() {

    $.ajax({
        url:'/rest/posts?title=' + $('#search_input').val(),
        method:'GET',
        dataType:'json',
        success:function(data) {

            for (var i = 0; i < data.length; i++) {

                var li = document.createElement('li');
                var id = data[i].id;
                var title = data[i].title;
                var user_id = data[i].user_id;
                var status = status_list[data[i].status];
                var status_style = status_style_list[data[i].status];
                var locker = data[i].locker_check;
                if (locker == 0) locker = "";
                var uname = "";
                var pN = null;

                    $.ajax({
                        url:'/rest/users/' + user_id + '/',
                        method:'GET',
                        dataType:'json',
                        async: false,
                        contentType:'application/json',
                        success:function(udata) {
                            uname = udata.uname;
                            pN = udata.phone_number;
                        }
                    });

                    li.innerHTML = "\
                    <div class='item'>\
                    <div class='name'>\
                      <span>" + uname + "</span>\
                    </div>\
                    <div class='phone'>\
                      <span>" + pN + "</span>\
                    </div>\
                    <div class='issue'>\
                      <span><a href=/home/product/" + id + "/>"  + title + "</a></span>\
                    </div>\
                    <div class='locker'>\
                      <span>" + locker + "</span>\
                    </div>\
                    <div class='status'>\
                      <span class='" + status_style + "'>" + status + "</span>\
                    </div>\
                    </div>";
                    table_body.appendChild(li);
                  

            }
        },
        error:function(err) {
            alert('검색 실패!');
        }
        });
        
    });