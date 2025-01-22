// Toggle navigation menu on small screens
function toggleNav() {
    var nav = document.getElementById("navMenu");
    if (nav.className === "nav") {
        nav.className += " responsive";
    } else {
        nav.className = "nav";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to the menu icon
    var menuIcon = document.getElementById("menuIcon");
    if (menuIcon) {
        menuIcon.addEventListener("click", toggleNav);
    }
});



document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.read-more-btn').forEach(button => {
        console.log('Attaching event listener to button'); // Debugging log
        button.addEventListener('click', () => {
            console.log('Button clicked'); // Debugging log
            const cardText = button.previousElementSibling.querySelector('.more-text');
            if (cardText) {
                console.log('Found more-text span'); // Debugging log
                const isHidden = cardText.style.display === 'none';
                cardText.style.display = isHidden ? 'inline' : 'none';
                button.textContent = isHidden ? 'Read Less' : 'Read More';
            } else {
                console.log('more-text span not found'); // Debugging log
            }
        });
    });
});

window.addEventListener('load', function() {
    document.querySelectorAll('.read-more-btn').forEach(button => {
        button.addEventListener('click', () => {
            const cardText = button.previousElementSibling.querySelector('.more-text');
            if (cardText) {
                const isHidden = cardText.style.display === 'none';
                cardText.style.display = isHidden ? 'inline' : 'none';
                button.textContent = isHidden ? 'Read Less' : 'Read More';
            }
        });
    });
});