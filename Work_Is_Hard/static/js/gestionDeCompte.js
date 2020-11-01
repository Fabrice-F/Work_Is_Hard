$("#modal_changementPseudo").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});
$("#modal_changementMotDePasse").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});

function ActiveBlockBackground()
{
    document.body.style.pointerEvents="none";
    document.getElementsByClassName("conteneur")[0].style.filter="blur(1.5rem)";
    Array.from(document.getElementsByClassName("modal")).forEach(fenetreModal => {
        fenetreModal.style.pointerEvents="auto";
    });
}

function disableBlockBackground()
{
    document.body.style.pointerEvents="auto";
    document.getElementsByClassName("conteneur")[0].style.filter="blur(0)";
}

function AjaxPseudo(baliseMessage)
{
    if (document.getElementById("PseudoVoulu").value=="")
    {
        PrintMessage(baliseMessage,"Le champs nouveau pseudo n'est pas remplit",true);
        return;
    }
    if (document.getElementById("pseudoUtilisateur").value==document.getElementById("PseudoVoulu").value)
    {
        PrintMessage(baliseMessage,"Le nouvezau pseudo est identique a l'ancien",true);
        return;
    }
    PseudoVoulu = document.getElementById("PseudoVoulu").value;
    $.ajax({
        url : '/DemandeSiPseudoDisponible', // La ressource ciblée
        type : 'POST', // Le type de la requête HTTP.
        data : `PseudoVoulu=${PseudoVoulu}` ,
        dataType : 'text', // On désire recevoir du text
        success : function(text, statut){ // contient le text renvoyé
        if (text=="True"){

            PrintMessage(baliseMessage,`Le pseudo a été actualisé, merci de vous reconnecter...`);
            document.getElementById("pseudoUtilisateur").value=PseudoVoulu;
            setTimeout(function(){
                document.getElementById("btnDeco").click();
            },2000)
        }
        else 
            PrintMessage(baliseMessage,text,true);
        },
       error : function(text, statut){ //  contient le text renvoyé
            alert("error: " +text)
        }
    });
}
function AjaxMotDePasse(baliseMessage)
{
    if (document.getElementById("AncienMotDePasse").value=="")
    {
        PrintMessage(baliseMessage,"Le champs ancien de mots de passe n'est pas remplit",true);
        return;
    }
    if (document.getElementById("NewMotDePasse").value=="")
    {
        PrintMessage(baliseMessage,"Le champs nouveau mot de passe n'est pas remplit",true);
        return;
    }
    if (document.getElementById("ConfirmationMotDePasse").value=="")
    {
        PrintMessage(baliseMessage,"Le champs confirmation mot de passe n'est pas remplit",true);
        return;
    }

    AncienMotDePasse = document.getElementById("AncienMotDePasse").value;
    NewMotDePasse = document.getElementById("NewMotDePasse").value;
    ConfirmationMotDePasse = document.getElementById("ConfirmationMotDePasse").value;
    
    if(NewMotDePasse!=ConfirmationMotDePasse){
        PrintMessage(baliseMessage,"Le mot de passe et la confirmation ne sont pas identique",true);
        return;
    }

    $.ajax({
        url : '/DemandeChangementPassword', // La ressource ciblée
        type : 'POST', // Le type de la requête HTTP.
        data : `AncienMotDePasse=${AncienMotDePasse}`+ `&NewMotDePasse=${NewMotDePasse}` + `&ConfirmationMotDePasse=${ConfirmationMotDePasse}` ,
        dataType : 'text', // On désire recevoir du text
        success : function(text, statut){ // contient le text renvoyé
        if (text=="True"){
            PrintMessage(baliseMessage,"Le mots de passe a été actualisé avec succès, merci de vous reconnecter...");
            document.getElementById("msgInchangeRole").value=PseudoVoulu;
            setTimeout(function(){
                document.getElementById("btnDeco").click();
            },2000)
        }
        else 
            PrintMessage(baliseMessage,text,true);
        },
       error : function(text, statut){ //  contient le text renvoyé
            alert("error: " +text)
        }
    });
}





function PrintMessage(element,message,error=false)
{
    document.getElementById(element).style.color="Green";
    document.getElementById(element).innerHTML=message;
    if(error)
        document.getElementById(element).style.color="Red";
    setTimeout(function(){
        document.getElementById(element).innerHTML="";
    },3000);
}