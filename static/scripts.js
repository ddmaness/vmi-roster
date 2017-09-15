

var view = {
    hideEmptyCard: function(id){
        var card = document.getElementById(id)
        if (card.firstChild.innerHTML == ""){
            card.style.display = "none";
        }
    }
}