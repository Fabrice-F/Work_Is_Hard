datePickerId=document.getElementById("dateNaissance");
year = new Date().getFullYear()-18
month = new Date().getMonth()
day = new Date().getDate()
datePickerId.max =new Date(year,month,day).toISOString().split("T")[0];

function EnvoiFormulaireInscription(){

    var NomFormulaire = document.getElementById("NomFormulaireInscription").value.trim();
    var PrenomFormulaire = document.getElementById("PrenomFormulaireInscription").value.trim();
    var PseudoFormulaire = document.getElementById("PseudoFormulaireInscription").value.trim();
    var mdp = document.getElementById("mot_de_passe").value.trim();
    var confirmation_mdp = document.getElementById("confirm_mdp").value.trim();
    var dateNaissance = document.getElementById("dateNaissance").value;

    //NOM: 
    if (isEmptyOrSpaces(NomFormulaire))
    {
        PrintMessage("msgErrorConfirmationInscription","Le champs nom est vide ...",true);
        return false;
    }

    if (!ifStringRespectcaracterNb(NomFormulaire,2,30)){
        PrintMessage("msgErrorConfirmationInscription","Le champs nom ne contient pas le nombre de caractères requis  ...",true);
        return false;
    }

    if (!isNomOrPrenomFormatCorrect(NomFormulaire))
    {
        PrintMessage("msgErrorConfirmationInscription","Le champs nom ne peut contenir que des lettres (sans espace ou chiffre) ...",true);
        return false;
    }

    //PRENOM:
    if(isEmptyOrSpaces(PrenomFormulaire)){
        PrintMessage("msgErrorConfirmationInscription","Le champs prenom est vide ...",true);
        return false;
    }

    if (!ifStringRespectcaracterNb(PrenomFormulaire,2,30)){
        PrintMessage("msgErrorConfirmationInscription","Le champs prenom ne contient pas le nombre de caractères requis  ...",true);
        return false;
    }

    if (!isNomOrPrenomFormatCorrect(PrenomFormulaire))
    {
        PrintMessage("msgErrorConfirmationInscription","Le champs prenom ne peut contenir que des lettres (sans espace ou chiffre) ...",true);
        return false;
    }
    
    //PSEUDO:
    if(isEmptyOrSpaces(PseudoFormulaire)){
        PrintMessage("msgErrorConfirmationInscription","Le champs pseudo est vide ...",true);
        return false;
    }
    if(!ifStringRespectcaracterNb(PseudoFormulaire,3,15)){
        PrintMessage("msgErrorConfirmationInscription","Le champs pseudo ne comporte pas le nombre de caractères requis ...",true);
        return false;
    }

    if (!isPseudoFormatCorrect(PseudoFormulaire))
    {
        PrintMessage("msgErrorConfirmationInscription","Le champs pseudo ne peut contenir que des lettres et des chiffres (sans espace)...",true);
        return false;
    }
    
    //MOTS DE PASSE:
    if(isEmptyOrSpaces(mdp)){
        PrintMessage("msgErrorConfirmationInscription","Le champs mot de passe est vide ou remplie d'espace ...",true);
        return false;
    }
    if(!isPasswordFormatCorrect(mdp)){
    
        PrintMessage("msgErrorConfirmationInscription","Le champs mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ...",true);
        return false;
    }
    
    //CONFIRM MDP:
    if(isEmptyOrSpaces(confirmation_mdp)){
        PrintMessage("msgErrorConfirmationInscription","Le champs confirmation de mots de passe  est vide ou remplie d'espace ...",true);
        return false;
    }
    if(!isPasswordFormatCorrect(confirmation_mdp)){
    
        PrintMessage("msgErrorConfirmationInscription","Le champs confirmation mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ...",true);
        return false;
    }
    
    //DATE DE NAISSANCE:
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
    var regularExpression = new RegExp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$");
    return regularExpression.test(str)
}

function isNomOrPrenomFormatCorrect(str)
{
    //var regularExpression = new RegExp(/^[A-Za-z\s]+$/); avec acceptation d'espace (dans le string)
    var regularExpression = new RegExp(/^[a-zA-Z]+$/); // sans acceptation d'espace
    return regularExpression.test(str)
}
function isPseudoFormatCorrect(str)
{
    var regularExpression = new RegExp(/^[a-z0-9]+$/i); // sans acceptation d'espace
    return regularExpression.test(str)
}

function ifStringRespectcaracterNb(str,min,max)
{
    if (str.length < min || str.length > max){
        return false;
    }
    return true;
}