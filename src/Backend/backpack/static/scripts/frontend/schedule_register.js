var search_input = document.querySelector("#search_input");
var table_body = document.querySelector(".table_body ul");

function search(){
  var span_items = document.querySelectorAll(".table_body .phone span");
  var search_item = search_input.value.toLowerCase();

  span_items.forEach(function(item){
    if(item.textContent.toLowerCase().indexOf(search_item) != -1){
       item.closest("li").style.display = "block";
    }
    else{
      item.closest("li").style.display = "none";
      }
  })
}

search_input.addEventListener("keyup", function(e){
  var span_items = document.querySelectorAll(".table_body .phone span");
  var search_item = e.target.value.toLowerCase();
 
  span_items.forEach(function(item){
   if(item.textContent.toLowerCase().indexOf(search_item) != -1){
      item.closest("li").style.display = "block";
   }
   else{
     item.closest("li").style.display = "none";
     }
 })
});

function register(id) {
    $.ajax({
        url: id + '/',
        method:'POST',
        data:{},
        success:function(data) {
            alert("등록 성공!")
        },
        error:function(jqXHR, textStatus, error) {
            alert(jqXHR.responseText);
        }
    });
}


// init
$.ajax({
  url:'/rest/courses/',
  method:'GET',
  dataType:'json',
  contentType:'application/json',
  success:function(data) {
    for (var i = 0; i < data.length; i++) {
      var li = document.createElement('li');
      var id = data[i].id;
      var cnumber = data[i].c_number;
      var cname = data[i].cname;
      var professor = data[i].professor;
      var ft = data[i].first_time;
      var st = data[i].second_time;
      var week = data[i].week;
      var time = ft + " - " + st + "\t" + week;

      li.innerHTML = "\
      <div class='item' type='button' onclick='register(" + id + ");'>\
      <div class='name'>\
        <span>" + cnumber + "</span>\
      </div>\
      <div class='phone'>\
        <span>" + cname + "</span>\
      </div>\
      <div class='issue'>\
        <span>" + time + "</a></span>\
      </div>\
      <div class='status'>\
        <span>" + professor + "</span>\
      </div>\
      </div>";
      table_body.appendChild(li);
    
    }
    search();

  },
  error:function(err) {
    alert('실패2');
  }
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

