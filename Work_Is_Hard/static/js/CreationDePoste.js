$("#modal_changementPseudo").iziModal({
    headerColor: '#00bfff',
});
$("#modal_changementMotDePasse").iziModal({
    headerColor: '#00bfff',
});


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

function EnvoyerOuPas()
{
    
    //TODO FAIRE UNE VERITABLE ALERTE
    if(window.Drapeau==false)
        alert("Le gif ou l'image n'est pas correctement formaté");
    TitrePoste = document.getElementById("TitrePoste").value;
    LienImg = document.getElementById("LienImg").value;

    if(isEmptyOrSpaces(TitrePoste) || isEmptyOrSpaces(LienImg)){
        alert("Un champs n'est pas renseigné")
        return false;      
    }
    else{
        if(window.Drapeau===true)
        {
            return true;
        }
    }
    return false;
}

function changeApercu(e,baliseChanger)
{
    parent = document.getElementById(baliseChanger).parentElement;
    balise = document.getElementById(baliseChanger);
    imageApercu = document.getElementById("apercuImg");
    if(baliseChanger =="apercuLegend"){
        balise.innerHTML=e.value;
    }
    else{
        if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(e.value))
        {
            imageApercu.src=e.value;
            imageApercu.style.visibility= "visible";
        }
    }
}

function onerrorApercu(bal)
{
    window.Drapeau=false;
    console.clear();
    bal.style.visibility= "hidden";
}

function succesApercu()
{
    window.Drapeau=true;
}
