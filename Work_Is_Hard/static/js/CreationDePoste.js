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

function isEmptyOrSpaces(str){
    return str === null || str.match(/^ *$/) !== null;
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