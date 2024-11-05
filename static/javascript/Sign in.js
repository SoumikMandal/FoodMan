document.addEventListener('DOMContentLoaded', function() {
    const wrapper = document.querySelector('.wrapper');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');

    registerLink.addEventListener('click', ()=> {
        wrapper.classList.add('active');
    });

    loginLink.addEventListener('click', ()=> {
        wrapper.classList.remove('active');
    });
});

function preventBack(){window.history.forward()};
setTimeout("preventBack()", 0);
    window.onunload=function(){null;}

function setcookie(){
    var u = document.getElementById('Username').value;
    var p = document.getElementById('Password').value;
    var r = document.getElementById('Role').value;

    document.cookie="username="+u+";path=http://127.0.0.1:8000/Sign%20in"
    document.cookie="password="+p+";path=http://127.0.0.1:8000/Sign%20in"
    document.cookie="role="+r+";path=http://127.0.0.1:8000/Sign%20in"
}

function getcookiedata(){
    var user = getCookie('username');
    var pwd = getCookie('password');
    var rl = getCookie('role');

    document.getElementById('Username').value=user;
    document.getElementById('Password').value=pwd;
    document.getElementById('Role').value=rl;
}

function getCookie(cname){
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++){
        var c = ca[i];
        while (c.charAt(0) == ' '){
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0){
            return c.substring(name.length, c.length);
        }
    }
    return "";
}