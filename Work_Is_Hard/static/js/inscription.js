datePickerId=document.getElementById("dateNaissance");
year = new Date().getFullYear()-18
month = new Date().getMonth()
day = new Date().getDate()
datePickerId.max =new Date(year,month,day).toISOString().split("T")[0];

function EnvoiFormulaireInscription(){

    var NomFormulaire = document.getElementById("NomFormulaireInscription").value;
    var PrenomFormulaire = document.getElementById("PrenomFormulaireInscription").value;
    var PseudoFormulaire = document.getElementById("PseudoFormulaireInscription").value;
    var mdp = document.getElementById("mot_de_passe").value;
    var confirmation_mdp = document.getElementById("confirm_mdp").value;
    var dateNaissance = document.getElementById("dateNaissance").value;


    if (isEmptyOrSpaces(NomFormulaire))
    {
        PrintMessage("msgErrorConfirmationInscription","Le champs nom est vide ou remplie d'espace ...",true);
        return false;
    }
    if(isEmptyOrSpaces(PrenomFormulaire)){
        PrintMessage("msgErrorConfirmationInscription","Le champs prenom est vide ou remplie d'espace ...",true);
        return false;
    }
    if(isEmptyOrSpaces(PseudoFormulaire)){
        PrintMessage("msgErrorConfirmationInscription","Le champs pseudo est vide ou remplie d'espace ...",true);
        return false;
    }
    if(PseudoFormulaire.length<5){
        PrintMessage("msgErrorConfirmationInscription","Le champs pseudo ne comporte pas 5 caractères ...",true);
        return false;
    }

    // rajouter max 15 caractère pour pseudo

    if(isEmptyOrSpaces(mdp)){
        PrintMessage("msgErrorConfirmationInscription","Le champs mot de passe est vide ou remplie d'espace ...",true);
        return false;
    }
    
    if(isEmptyOrSpaces(confirmation_mdp)){
        PrintMessage("msgErrorConfirmationInscription","Le champs confirmation de mots de passe  est vide ou remplie d'espace ...",true);
        return false;
    }    

    if(!isPasswordFormatCorrect(mdp)){
    
        PrintMessage("msgErrorConfirmationInscription","Le champs mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ...",true);
        return false;
    }
    // tester si confirme format correct


    if(isEmptyOrSpaces(dateNaissance)){
        PrintMessage("msgErrorConfirmationInscription","Le champs date de naissance n'est pas remplie ... ",true);
        return false;
    }

    if(mdp == confirmation_mdp){
        return true;
    }
    else{
        PrintMessage("msgErrorConfirmationInscription","Les mots de passe sont differents ...",true);
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

function isPasswordFormatCorrect(str)
{
    var regularExpression = new RegExp(/^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$/);

    return regularExpression.test(str)
}