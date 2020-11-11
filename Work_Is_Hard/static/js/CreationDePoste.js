function EnvoyerOuPas()
{
    
    //TODO FAIRE UNE VERITABLE ALERTE
    if(window.Drapeau==false)
        PrintMessage("msgPubliePost","L'adresse du gif ou de l'image n'est pas correctement formaté",true,5000);
    TitrePoste = document.getElementById("TitrePoste").value;
    LienImg = document.getElementById("LienImg").value;

    if(isEmptyOrSpaces(TitrePoste) || isEmptyOrSpaces(LienImg)){
        PrintMessage("msgPubliePost","Un champs n'est pas renseigné",true);
        return false;      
    }
    else{
        if(window.Drapeau===true)
        {
            document.getElementById("LienImg").disabled=false;
            return true;
        }
    }
    return false;
}

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

    //if((/\.(gif|jpg|jpeg|tiff|png)$/i).test(this.value)) 
    var regex= new RegExp('https?://(?:[a-z0-9\-]+\.)+[a-z0-9]{2,6}(?:/[^/#?]+)+\.(?:jpg|jpeg|gif|png)$')
    if(regex.test(this.value)) 
    {
        imageApercu = document.getElementById("apercuImg");
        imageApercu.src=this.value;
        imageApercu.style.visibility= "visible";
        document.getElementById("btnClear").style.display = "flex";
        document.getElementById("LienImg").disabled=true;

        document.getElementById("btnClear").addEventListener("click",function(){
            imageApercu.src="";
            document.getElementById("LienImg").value="";
            document.getElementById("btnClear").style.display = "none";
            document.getElementById("btnClear").removeEventListener("click");
            document.getElementById("LienImg").disabled=false;
        });

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
