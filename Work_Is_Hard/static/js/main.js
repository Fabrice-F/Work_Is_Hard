function EnvoyerOuPas()
{
    TitrePoste = document.getElementById("TitrePoste").value;
    LienImg = document.getElementById("LienImg").value;

    if(isEmptyOrSpaces(TitrePoste) || isEmptyOrSpaces(LienImg)){
        alert("Un champs n'est pas renseigné")
        return false;      
    }
    else{
        
        alert(TitrePoste);
        alert(LienImg)
        return true;
    }
}



function isEmptyOrSpaces(str){
    return str === null || str.match(/^ *$/) !== null;
}

function changeApercu(e,baliseChanger)
{
    parent = document.getElementById(baliseChanger).parentElement;
    balise = document.getElementById(baliseChanger);
    if(baliseChanger =="apercuLegend"){
        balise.innerHTML=e.value;
    }
    else{
        if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(e.value))
        {
            balise.remove();
            parent.innerHTML +=`<img src="${e.value}" class="gif" alt="test" id="apercuImg" onerror="this.style.display='none'">`;
    
        }
    }


}