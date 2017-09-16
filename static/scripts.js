

var view = {
    hideEmptyCard: function(id){
        card = document.getElementById(id)
        if (card.firstChild.innerHTML == ""){
            card.style.display = "none";
        }
    }
}

var handlers = {
    goBack: function(){
        window.history.back();
    },
    loginValidation: function(username, password){
        username = document.getElementsByName(username);
        password = document.getElementsByName(password);
        if (username[0].value == "" && password[0].value == ""){
            username[0].placeholder = "USERNAME REQUIRED";
            password[0].placeholder = "PASSWORD REQUIRED";
            return false;
        }
        if (username[0].value == ""){
            username[0].placeholder = "USERNAME REQUIRED";
            return false;
        }
        if (password[0].value == ""){
            password[0].placeholder = "PASSWORD REQUIRED";
            return false;
        }
    },
    addCadetValidation: function(firstName, lastName){
        first = document.getElementsByName(firstName);
        last = document.getElementsByName(lastName);
        if (first[0].value == "" && last[0].value == ""){
            first[0].placeholder = "FIRST NAME REQUIRED";
            last[0].placeholder = "LAST NAME REQUIRED";
            return false;
        }
        if (first[0].value == ""){
            first[0].placeholder = "FIRST NAME REQUIRED";
            return false;
        }
        if (last[0].value == ""){
            last[0].placeholder = "LAST NAME REQUIRED";
            return false;
        }
    }
}

window.onload = view.hideEmptyCard("confirm_check_in")