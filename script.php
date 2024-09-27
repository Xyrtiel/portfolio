<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $comment = $_POST['comment'];

    $entry = "Nom: $name, Email: $email, Commentaire: $comment\n";

    file_put_contents('infos.txt', $entry, FILE_APPEND); 

    echo "Commentaire enregistré avec succès.";
} else {
    echo "Méthode non autorisée.";
}
?>
