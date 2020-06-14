var search_input = document.querySelector("#search_input");
var table_body = document.querySelector(".table_body ul");
var status_list = ["판매중", "판매완료"];
var status_style_list = ["open", "closed"];

function search(){
  var span_items = document.querySelectorAll(".table_body .issue span");
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
  var span_items = document.querySelectorAll(".table_body .issue span");
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


// init
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
    search();

  },
  error:function(err) {
    alert('실패2');
  }
});


