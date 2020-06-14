var category = document.getElementById('category');
var stats = document.getElementById('status');
var locker_update_flag = 0;
var checked_locker_id = 0;
var checked_index = -1;

$('#btn_register').on('click', function() {
    var post_id = 0;
    var cg = category.value;
    var file = $('#reportFile').val();
    var strFileName = file.replace(/^.+?\\([^\\]+?)(\.[^\.\\]*?)?$/gi, "$1");
    var FileExt = file.replace(/.+\./, "");
    var filename = strFileName + '.' + FileExt;

    if (file == "") {
        alert("사진을 추가해주세요!");
        return;
    }

    $.ajax({
        url:'/rest/posts/',
        method:'POST',
        dataType:'json',
        data:{
            'title':$('#title').val(),
            'content':$('#content').val(),
            'locker_check': checked_locker_id
        },
        success:function(data) {
            var formdata = new FormData();
            var myfile = $('#reportFile')[0].files[0];
            post_id = data;

            formdata.append('name', filename);
            formdata.append('file', myfile);
            formdata.append('pname', $('#product_name').val());
            formdata.append('price', $('#price').val());
            formdata.append('post_id', post_id);
            formdata.append('category', cg);

            $.ajax({
                url:'/upload_product/',
                method:'POST',
                processData: false,
                contentType: false,
                data: formdata,
                success:function(data) {

                    // 사물함 사용 시 변경
                    if(checked_locker_id != 0){
                        $.ajax({
                            url:'/rest/lockers/' + checked_locker_id + '/',
                            method:'PATCH',
                            data: {'status': 1},
                            success:function(data) {
                                console.log("사물함 사용 저장 성공");
                            },
                            error:function(err) {
                                alert('사물함 사용 저장 실패');
                            }
                        });
                    }

                    alert("저장 완료!")
                    window.location.replace('/home/transaction/');
                },
                error:function(err) {
                    alert('저장에 실패!, 다시 시도!2');
                }
            });
        },
        error:function(err) {
            alert('저장에 실패!, 다시 시도!1');
        }
    });
});

// function showPopup() { window.open("pop_up", "a", "width=400, height=300, left=100, top=50"); }
function close_popup(){
    var popup = document.getElementsByClassName('popup');
    popup[0].style.display = 'none';
}

function get_locker_list(){
    var popup = document.getElementsByClassName('popup');
    popup[0].style.display = 'block';

    if(locker_update_flag == 0){
        $.ajax({
            url:'/rest/lockers/',
            method:'GET',
            dataType:'json',
            success:function(data){
                locker_update_flag = 1;
                console.log(data);

                var table = document.getElementById('table_body');

                for (var i = 0; i < data.length; i++) {
        
                    var tr = document.createElement('tr');
                    
                    var locker_id = data[i].id;
                    var locker_number = data[i].l_number;
                    var locker_status = data[i].status;
                    var locker_location = data[i].location;
        
                    
                    if (locker_status == 0){
                        tr.innerHTML = "<td width='20%' align='center' name='locker_number'>" 
                            + locker_number + "</td><td width='20%' align='center'>" 
                            + locker_status + "</td>" 
                            + "<td width='40%' align='center'>" + locker_location +  "</td>" 
                            + "<td width='20%' align='center'>\
                            <input type='radio' name='locker_status_check'></td>"
                    }else{
                        tr.innerHTML = "<td width='20%' align='center' name='locker_number'>" 
                            + locker_number + "</td><td width='20%' align='center'>" 
                            + locker_status + "</td>" 
                            + "<td width='40%' align='center'>" + locker_location +  "</td>" 
                            + "<td width='20%' align='center'><input type='radio' disabled='true' name='locker_status_check'></td>"
                    }
        
                    

                    table.appendChild(tr);
                
                }
    
            }
        })
}
}

$('#btn_update').on('click', function() {
    var post_id = $('#post_id').val();
    var product_id = $('#product_id').val();
    var cg = category.value;
    var stat = stats.value;
    var locker_check = $('#locker_check').val();
    var file = $('#reportFile').val();
    var strFileName = file.replace(/^.+?\\([^\\]+?)(\.[^\.\\]*?)?$/gi, "$1");
    var FileExt = file.replace(/.+\./, "");
    var filename = strFileName + '.' + FileExt;

    if (checked_locker_id != 0) var updated_locker = checked_locker_id;
    else var updated_locker = locker_check;
    if (stat == 1) var updated_locker = 0;

    $.ajax({
        url:'/rest/posts/' + post_id + "/",
        method:'PUT',
        dataType:'json',    
        data:{
            'id':post_id,
            'title':$('#title').val(),
            'content':$('#content').val(),
            'status':stat,
            'locker_check':updated_locker
        },
        success:function(data) {
            var formdata = new FormData();
            var myfile = $('#reportFile')[0].files[0];

            formdata.append('name', filename);
            formdata.append('file', myfile);
            formdata.append('pname', $('#product_name').val());
            formdata.append('price', $('#price').val());
            formdata.append('post_id', post_id);
            formdata.append('product_id', product_id);
            formdata.append('category', cg);

            $.ajax({
                url:'/upload_product/',
                method:'POST',
                processData: false,
                contentType: false,
                data: formdata,
                success:function(data) {

                    // 이전 사물함 할당 해제
                    if (updated_locker != locker_check && locker_check != 0) {
                        $.ajax({
                            url:'/rest/lockers/' + locker_check + '/',
                            method:'PATCH',
                            data: {'status': 0},
                            success:function(data) {
                                // console.log("사물함 사용 저장 성공");
                            },
                            error:function(err) {
                                // alert('사물함 사용 저장 실패');
                            }
                        });
                    }

                    // 사물함 사용 시 변경
                    if(updated_locker != 0){
                        $.ajax({
                            url:'/rest/lockers/' + updated_locker + '/',
                            method:'PATCH',
                            data: {'status': 1},
                            success:function(data) {
                                // console.log("사물함 사용 저장 성공");
                            },
                            error:function(err) {
                                // alert('사물함 사용 저장 실패');
                            }
                        });
                    }

                    window.location.replace('/home/transaction/');
                    alert("저장 완료!")
                },
                error:function(err) {
                    alert('저장에 실패!, 다시 시도!2');
                }
            });
        },
        error:function(err) {
            alert('저장에 실패!, 다시 시도!1');
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


$('#btn_choose').on('click', function() {
    var radio = document.getElementsByName('locker_status_check');

    
    for(var i = 0; i < radio.length; i++){
        if(radio[i].checked==true){
            checked_index = i;
        }
    }

    if(checked_index == -1){
        alert("사용할 사물함을 선택하세요!");
    }
    else{
        var locker_num = document.getElementsByName('locker_number');
        locker_name = locker_num[checked_index].childNodes[0].nodeValue

        $.ajax({
            url:'/rest/lockers?l_number=' + locker_name,
            method:'GET',
            dataType:'json',    
            success:function(data) {
                checked_locker_id = data[0].id;
                alert("사물함 선택 완료!");
            },
            error:function(err){
                alert("사물함 선택 실패!");
            }
        });



       
    }
    
    
   
});
