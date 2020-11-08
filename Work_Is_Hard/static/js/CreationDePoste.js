
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

/*function changeApercu(e,baliseChanger)
{
    parent = document.getElementById(baliseChanger).parentElement;
    balise = document.getElementById(baliseChanger);
    imageApercu = document.getElementById("apercuImg");


    if(baliseChanger =="apercuLegend"){
        console.log(e.textContent || e.innerText);
        balise.innerHTML=e.value.replace(/[&\/\\#,+()$~%.:*<>{}]/g, '');
    }
    else{
        //e= e.value.replace(/[#,+()$~%.'":*?<>{}]/g, '');
        if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(e.value)) //replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, '');
        {
            imageApercu.src=e.value;
            imageApercu.style.visibility= "visible";
        }
    }
}*/


$('#TitrePoste').on('input', function() {
    var c = this.selectionStart,
        v = $(this).val();
    if((/[\/\\()~*<>{}]/g).test(v)) {
        $(this).val(v.replace(/[&\/\\#,+()$~%.:*<>{}]/g, ''));
        c--;
    }
    this.setSelectionRange(c, c);
    document.getElementById("apercuLegend").innerHTML=this.value;
});

$('#LienImg').on('input', function() {
    var c = this.selectionStart,
        v = $(this).val();
    if((/[,()~*<>{}]/g).test(v)) {
        $(this).val(v.replace(/[&\/\\#,+()$~%.:*<>{}]/g, ''));
        c--;
    }
    this.setSelectionRange(c, c);
    if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(this.value)) //replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, '');
    {
        imageApercu = document.getElementById("apercuImg");
        imageApercu.src=this.value;
        imageApercu.style.visibility= "visible";
        document.getElementById("LienImg").disabled = true;
    }
});



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
