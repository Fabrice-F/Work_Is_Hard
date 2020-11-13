
/* === GENERAL A LA PAGE  === */
new CBPFWTabs( document.getElementById( 'tabs' ) );

$("#modal_changeRole").iziModal({
    closeButton: true,
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});

$("#modalMsgInfo").iziModal({
    closeButton: true,
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});

$("#modalModeModeration").iziModal({
    closeButton: true,
    headerColor: '#00bfff',
    onOpening: ActiveBlockBackground,
    onClosing: disableBlockBackground,
});


/* === PARTIE ATTRIBUTION ROLE === */
function openModalChangeRole(idUser,pseudo,ancienRole)
{
    NouveauRole = document.querySelector(`input[name="roleUtilisateur${idUser}"]:checked`).value;
    
    if(NouveauRole==ancienRole)
    {
        PrintMessage("msgInchangeRole","L'ancien Rôle est équivalent au nouveau poste",true);
        document.getElementById("OpenModal"+idUser).click();
        return 
    }

    msgRappel=`Êtes-vous sur de vouloir changer le rôle de ${pseudo} ?`;
    msgAncienRole=`<span class="RoleAccentuation"> ${ancienRole}</span> `;
    msgNouveauRole=`<span class="RoleAccentuation"> ${NouveauRole}</span> `;

    document.getElementById("msgRappel_changeRole").innerHTML= msgRappel;
    document.getElementById("msgAncienRole_changeRole").innerHTML= "Ancien Role: " + msgAncienRole;
    document.getElementById("msgNouveauRole_changeRole").innerHTML="Nouveau Role: " + msgNouveauRole;

    document.getElementById("OpenModal"+idUser).click();

    document.getElementById("btnValideChangeRole").addEventListener('click', function(){
        ValidChangeRole(pseudo,idUser,ancienRole,NouveauRole);
    });

}

    // Implemente AJAX
function ValidChangeRole(pseudo,id,ancienRole,NouveauRole)
{
    AdminPwd = document.getElementById("mdpChangeRole").value
    baliseMessage ="msgInchangeRole";
    
    if(isEmptyOrSpaces(AdminPwd))
    {
        PrintMessage(baliseMessage,"Le champs mot de passe est vide",true);
        return
    }

    $.ajax({
        url : '/changement_role', // La ressource ciblée
        type : 'POST', // Le type de la requête HTTP.
        data : `pseudoUser=${pseudo}&idUser=${id}&AncienRoleUser=${ancienRole}&NouveauRoleUser=${NouveauRole}&AdminPwd=${AdminPwd}` ,
        dataType : 'text', // On désire recevoir du text
        success : function(text, statut){ // contient le text renvoyé
        if (text=="True"){
            PrintMessage(baliseMessage,`Le role a été actualisé, rechargement de la page dans 2 secondes...`);
            setTimeout(function(){
                window.location.reload();
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


/* === PARTIE MESSAGE INFORMATION === */
function sendMsgInformation(baliseMessageInModal)
{
    Msg = document.getElementById("txtAreaMsgInfo").value;
    MdpUser = document.getElementById("mdpMsgInfo").value;

    if(isEmptyOrSpaces(Msg)){
        PrintMessage(baliseMessageInModal,"Le message d'information est vide, veuillez le remplir",true);
        return;
    }

    if(isEmptyOrSpaces(MdpUser)){
        PrintMessage(baliseMessageInModal,"Le champs mot de passe est vide ...",true);
        return;
    }
    SendAjax("/update_msg_information","message d'information",baliseMessageInModal,Msg,MdpUser);
}


function openModalModeModeration(inputToggle,isModeActiveBdd)
{
    statusActuel = isModeActiveBdd ? 'activé' : 'désactivé' ;
    ModeModerationVoulu = document.getElementById(inputToggle).checked;
    if(String(ModeModerationVoulu).toLowerCase()==String(isModeActiveBdd).toLowerCase())
    {
        PrintMessage("msgErrorModeModeration",`Le mode modération est déja ${statusActuel} actuellement !`,true);
        return;
    } 

    statusVoulu = ModeModerationVoulu ? 'activé' : 'désactivé' ;
    document.getElementById("msgRappeModeModeration").innerHTML="Étes vous sur de vouloir passer en mode ?"
    document.getElementById("msgNouveauRole_ModeModeration").innerHTML=statusVoulu;
    $('#modalModeModeration').iziModal('open');
}

function sendModeModeration(baliseMsgInModal,baliseInputModeModerationVoulut)
{
    MdpUser = document.getElementById("mdpModeModeration").value;
    ModeModerationVoulu = document.getElementById(baliseInputModeModerationVoulut).checked;
    if(isEmptyOrSpaces(MdpUser)){
        PrintMessage(baliseMsgInModal,"Le champs mot de passe est vide ...",true);
        return;
    }

    ModeModerationVoulu = new String(ModeModerationVoulu);
    SendAjax("/changement_mode_moderation","mode modération",baliseMsgInModal,MdpUser,ModeModerationVoulu)
}