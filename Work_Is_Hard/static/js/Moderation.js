$("#modalPAM").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});


function choixValidPAM(isAccept,idPoste){
    console.log("Poste id ? " + idPoste)
    console.log("Poste accepter ? " + isAccept)
}

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