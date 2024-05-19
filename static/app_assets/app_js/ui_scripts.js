// When the user clicks the button, toggle between hiding and showing the dropdown content.
function showMenu() {
    document.getElementById("dropdownBox").classList.toggle('show');
}

// Close dropdown if user clicks outside of it.
window.onclick = function(e) {
    if(!e.target.matches('.dropbtn')) {
        var dropdownBox = document.getElementById("dropdownBox");
        if(dropdownBox.classList.contains('show'))  {
            dropdownBox.classList.remove('show');
        }
    }
}