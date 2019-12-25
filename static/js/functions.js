function send_answer(user_id, question_id, answer) {
    // no need to be secure
    var http = new XMLHttpRequest();
    var url = '/select_answer';
    var params = 'user_id=' + user_id + '&question_id=' + question_id + '&answer=' + answer;
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            window.location.replace('/answered')
        }
    }
    http.send(params);
}

function delete_userID() {
    document.cookie = "user_id=; expires=Thu, 01 Jan 2000 00:00:00 GMT";
    window.location.replace('/register')
}