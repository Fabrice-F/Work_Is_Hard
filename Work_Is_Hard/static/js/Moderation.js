$("#modalPAM").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});

$("#modal_confirmStatusPAM").iziModal({
    background: '#00bfff',
    closeButton: true,
    bottom: '0px',
    onOpening: ModalTimeClose
});

function openModalBanUser(userId,userPseudo){
    //TODO : test si l'utilisateur de la session 
    //est le meme que celui a bannir
    $("#modalPAM").iziModal('open');

    document.getElementById("msgRappePAM").innerHTML="Vous allez bannir l'utilisateur avec le pseudo:";
    document.getElementById("msgNouveauRole_PAM").innerHTML=userPseudo;

    console.log("Utilisateur a bannir:" +userId );

    document.getElementById("btnValidePAM").addEventListener('click', function(){
        sendBanissementPAM("msgInModalPAM",userId);
    });
}

function sendBanissementPAM(baliseMsgInModal,user_id)
{
    MdpUser= document.getElementById("mdpPAM").value;

    if(isEmptyOrSpaces(MdpUser)){
        PrintMessage(baliseMsgInModal,"Votre mots de passe est vide ...",true);
        return;
    }
    userId = String(user_id)
    SendAjax("/Bannissement","status de l'utilisateur",baliseMsgInModal,userId,MdpUser);
}

function choixValidPAM(isPostAccept,idPoste){

    $.ajax({
        url : "/updatePosteAttenteModeration", // La ressource ciblée
        type : 'POST', // Le type de la requête HTTP.
        data : `idPoste=${idPoste}&isPostAccept=${isPostAccept}`,
        dataType : 'text', // On désire recevoir du text
        success : function(text, statut){ // contient le text renvoyé
        if (text=="True"){

            document.getElementById("paragrapheConfirmStatusPAM").innerHTML="Le poste à été actualiser, actualisation dans 3s...";
            $("#modal_confirmStatusPAM").iziModal('open');
            
            setTimeout(function(){
                window.location.reload();
            },3000)
        }
        else 
            document.getElementById("paragrapheConfirmStatusPAM").innerHTML =text;
            $("#modal_confirmStatusPAM").iziModal('open');
        },
        error : function(text, statut){ //  contient le text renvoyé
            alert("error: " +text)
        }
    });
}

function ModalTimeClose()
{
    setTimeout(function(){
        $('#modal_confirmStatusPAM').iziModal('close');
    },2000); 
}