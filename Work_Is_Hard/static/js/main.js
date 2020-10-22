var drapeauGifOk ={value:""};

$("#modal").iziModal({
    headerColor: '#00bfff',
});

function EnvoyerOuPas()
{
    alert("value drapeau: "+drapeauGifOk.value)
    TitrePoste = document.getElementById("TitrePoste").value;
    LienImg = document.getElementById("LienImg").value;

    if(isEmptyOrSpaces(TitrePoste) || isEmptyOrSpaces(LienImg)){
        alert("Un champs n'est pas renseigné")
        return false;      
    }
    else{
        if(drapeauGifOk.value===true)
        {
            alert(TitrePoste);
            alert(LienImg)
            return true;
        }
    }
}

function isEmptyOrSpaces(str){
    return str === null || str.match(/^ *$/) !== null;
}

function changeApercu(e,baliseChanger)
{
    drapeauGifOk.value ="";
    parent = document.getElementById(baliseChanger).parentElement;
    balise = document.getElementById(baliseChanger);
    imageApercu = document.getElementById("apercuImg");
    if(baliseChanger =="apercuLegend"){
        balise.innerHTML=e.value;
    }
    else{
        if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(e.value))
        {
            //balise.remove();
            imageApercu.src=e.value;
            imageApercu.style.visibility= "visible";
            //parent.innerHTML +=`<img src="${e.value}" class="gif" alt="test" id="apercuImg" onerror="this.style.display='none'">`;
        }
    }
}
function onerrorApercu(e,bal)
{
    drapeauGifOk.value=false;
    console.clear();
    bal.style.visibility= "hidden";
}
function succesApercu()
{
    drapeauGifOk.value=true;
    console.log("ok");
}