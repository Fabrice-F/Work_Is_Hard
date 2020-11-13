$("#modalPAM").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});


$("#modalConfirmationStatusChoixPAM").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});

$("#modalChangementTitrePoste").iziModal({
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
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
    userId = new String(user_id)
    SendAjax("/banissement","status de l'utilisateur",baliseMsgInModal,userId,MdpUser);
}

function choixValidPAM(isPostAccept,idPoste){

    status = isPostAccept ? "Accepté" : "Refusé" ;
    document.getElementById("msgConfirmationStatusChoixPAM").innerHTML=status;

    $("#modalConfirmationStatusChoixPAM").iziModal('open');
    
    document.getElementById("btnValideConfirmationStatusChoixPAM").addEventListener("click",function(){
        sendChoixValidPAM(isPostAccept,idPoste);
    });
}

function sendChoixValidPAM(isPostAccept,idPoste)
{

    baliseMsgInModal="msgInModalConfirmationStatusChoixPAM";

    IdPoste = new String(idPoste);
    IsPostAccept = new String(isPostAccept);
    SendAjax("/update_poste_attente_moderation","poste",baliseMsgInModal,IdPoste,IsPostAccept)
}


function changeTitrePAM(idPoste)
{
    AncientitrePostePAM=document.getElementById("titrePAM"+idPoste).innerHTML;
    document.getElementById("AncienTitrePoste").innerHTML =AncientitrePostePAM;
    document.getElementById("NouveauTitrePoste").value =AncientitrePostePAM;

    $("#modalChangementTitrePoste").iziModal('open');

    document.getElementById("btnValideChangementTitrePoste").addEventListener("click",function(){
        sendNewTitrePAM(idPoste);
    });
}

function sendNewTitrePAM(idPoste){

    baliseMsgInModal="msgInModalChangementTitrePoste";
    newTitrePoste = document.getElementById("NouveauTitrePoste").value;

    MdpUser = document.getElementById("mdpChangementTitrePoste").value;

    if(isEmptyOrSpaces(MdpUser)){
        PrintMessage(baliseMsgInModal,"Votre mots de passe est vide ...",true);
        return;
    }
    
    if(isEmptyOrSpaces(newTitrePoste)){
        PrintMessage(baliseMsgInModal,"Le titre est vide ...",true);
        return;
    }

    IdPoste = new String(idPoste);
    NewTitrePoste = new String(newTitrePoste);
    SendAjax("/update_titre_pam","titre du poste",baliseMsgInModal,IdPoste,NewTitrePoste,MdpUser)
}