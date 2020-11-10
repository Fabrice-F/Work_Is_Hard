function EnvoiFormulaireInscription(){
    var mdp = document.getElementById("mot_de_passe").value;
    var confirmation_mdp = document.getElementById("confirm_mdp").value;
    
    if(mdp == confirmation_mdp){
        return true;
    }else{
        alert("les mots de passe sont differents");
        return false;
    }
}

function ChampsVide(){
    var nom = document.getElementById("NomFormulaireInscription").value;
    var prenom = document.getElementById("PrenomFormulaireInscription").value;
    var pseudo = document.getElementById("PseudoFormulaireInscription").value;
    const regex = /[A-Za-z0-9]/g;

    if(nom || prenom || pseudo % regex){
        PrintMessage("msgErrorConfirmationInscription","Les caractères entré dans les champs ne sont pas valide.", true);
    }else{
        return false 
    }

    if(isEmptyOrSpaces(nom)){
            PrintMessage("msgErrorConfirmationInscription","Votre champ nom est vide",true);
            return false;
    }else if(isEmptyOrSpaces(prenom)){
        PrintMessage("msgErrorConfirmationInscription","Votre champ prénom est vide",true);
        return false;
    }else if(isEmptyOrSpaces(pseudo)){
        PrintMessage("msgErrorConfirmationInscription","Votre champ pseudo est vide",true);
        return false;
    }
    return false;
}