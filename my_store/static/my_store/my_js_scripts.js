function changeVisibility(attr) {
  let x = document.getElementById("id_password");
  if (x.type === "password") {
    x.type = "text";
    attr.src ="/static/my_store/img/iconmonstr-eye-9-24.png";
  } else {
    x.type = "password";
    attr.setAttribute('src', "/static/my_store/img/iconmonstr-eye-10-24.png" );
    
  }
}

let checks = document.getElementsByClassName('password_visibility');

for(let i=0; i <= checks.length - 1; i++)
{
  checks[i].addEventListener('click', function() {changeVisibility(checks[i])});
}
