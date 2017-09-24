

var view = {
    hideEmptyCard: function(id){
        //if an element is empty switch display to "none"
        card = document.getElementById(id)
        if (card.firstChild.innerHTML == ""){
            card.style.display = "none";
        }
    }
}

var handlers = {
    goBack: function(){
        //return to previous page
        window.history.back();
    },
    loginValidation: function(username, password){
        //capture username and password input
        username = document.getElementsByName(username);
        password = document.getElementsByName(password);
        //check for empty inputs on username and password
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
        //capture first and last name
        first = document.getElementsByName(firstName);
        last = document.getElementsByName(lastName);
        //check for empty inputs in input fields
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
    },
    expandMenuTray:function(){
        //toggle class of off screen nav bar to "open" when function runs to display it
        var tray = document.querySelector(".off_screen_nav")
        tray.classList.toggle('open');
        event.stopPropagation();
    },
    closeMenuTray:function(){
        //remove class "open" off screen nav to move it off screen when run
        var tray = document.querySelector(".off_screen_nav")
        tray.classList.remove('open');
    }
}
//hides the confirm check in card on the initial loading of the add.html screen
window.onload = view.hideEmptyCard("confirm_check_in");