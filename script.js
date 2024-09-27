document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const name = this.name.value;
    const email = this.email.value;
    const comment = this.comment.value;


    const messageDiv = document.getElementById('message');
    messageDiv.textContent = 'Votre commentaire est en cours d\'enregistrement...';
    messageDiv.style.color = 'blue';
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'process.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            messageDiv.textContent = 'Votre commentaire a bien été enregistré !';
            messageDiv.style.color = 'green'; 
            console.log('Commentaire enregistré avec succès');
        } else {
            messageDiv.textContent = 'Erreur lors de l\'enregistrement du commentaire.';
            messageDiv.style.color = 'red'; 
            console.error('Erreur lors de l\'enregistrement du commentaire');
        }
    };
    xhr.send(`name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&comment=${encodeURIComponent(comment)}`);

    this.reset();
});
