
$("#modal_changementPseudo").iziModal({
    headerColor: '#00bfff',
});
$("#modal_changementMotDePasse").iziModal({
    headerColor: '#00bfff',
});

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

function CopyLinkImage(button){
    var copyText = button.parentNode.parentNode.children[1].children[1] ;
    const el = document.createElement('textarea');
    el.value = copyText.src;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    AnimationBtnFlipIn(button)
}
function AnimationBtnFlipIn(bouton)
{
    bouton.classList.add("animate__flipInX");
    setTimeout(function() { bouton.classList.remove("animate__flipInX");}, 1000);
}

function Get()
{

    $.ajax('/testAjax',   // request url
    {
        success: function (data, status, xhr) {// success callback function
            $('#test').append(data);
        }
    });

       

    
}