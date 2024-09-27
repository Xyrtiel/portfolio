// Fonction qui permet d'ouvrir un onglet :
/* ---------------------------------------------------------------------------------------------------------------------- */
// Déclaration d'une variable pour stocker l'onglet précédemment cliqué
var ongletPrecedent = null;

// Fonction qui permet d'ouvrir un onglet
function openOnglet(evt, name) {
    var i, contenu_onglets, ongletlinks;

    // Récupération des éléments de la classe contenu_onglets
    contenu_onglets = document.getElementsByClassName('contenu_onglets');
    for (i = 0; i < contenu_onglets.length; i++) {
        contenu_onglets[i].style.display = 'none'; // Masquer tous les contenus des onglets
    }

    // Récupération des éléments de la classe ongletlinks
    ongletlinks = document.getElementsByClassName('ongletlinks');
    for (i = 0; i < ongletlinks.length; i++) {
        ongletlinks[i].classList.remove("active"); // Réinitialiser tous les onglets en supprimant la classe "active"
    }

    // Réinitialisation de la couleur de l'onglet précédemment cliqué
    if (ongletPrecedent !== null) {
        ongletPrecedent.classList.remove("active"); // Supprimer la classe "active" de l'onglet précédent
    }

    // Affichage du contenu de l'onglet sélectionné
    document.getElementById(name).style.display = "block";
    // Ajout de la classe "active" à l'élément courant
    evt.currentTarget.classList.add("active");
    // Stockage de l'onglet actuellement cliqué
    ongletPrecedent = evt.currentTarget;
}




