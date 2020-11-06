$("#modal_CopieOK").iziModal({
    background: '#1E8449',
    closeButton: true,
    bottom: '0px',
    onOpening: ModalCopyOpen
});


function CopyLinkImage(button){
    var copyText = button.parentNode.parentNode.children[1].children[1].children[0]  ;
    const el = document.createElement('textarea');
    el.value = copyText.src;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}

function ModalCopyOpen()
{
    document.getElementById("imgModal").src="../static/img/Check-gif.gif";
    setTimeout(function(){
        $('#modal_CopieOK').iziModal('close')
        document.getElementById("imgModal").src="";
    },1500); 
}

function moderationDirection(ValueSelectChoix,idPoste,idUserPoste,PseudoPosteur)
{
    // console.log("ValueSelectChoix:" +ValueSelectChoix);
    console.log("idPoste:" +idPoste);
    // console.log("idUserPoste:" +idUserPoste);
    // console.log("PseudoPosteur:" +PseudoPosteur);
    // console.log("TitrePoste :" +TitrePoste);
    TitrePoste = document.getElementById("titrePoste"+idPoste).innerHTML;
    switch (ValueSelectChoix) {

        case "1":
            CorrectionTitrePoste(TitrePoste,idPoste);
            break;

        case "2":
            SuppressionPoste(idPoste,PseudoPosteur);
            break;

        case "3":
            BanUser(idUserPoste,PseudoPosteur);
            break;
    
        default:
            alert("Une erreur a eut lieu contacter les développeurs");
            break;
    }
}

function CorrectionTitrePoste(TitrePoste,idPoste)
{
    document.getElementById("AncienTitrePoste").innerHTML=TitrePoste;
    document.getElementById("NouveauTitrePoste").value=TitrePoste;
    $("#modalChangementTitrePoste").iziModal('open');

    document.getElementById("btnValideChangementTitrePoste").addEventListener('click',function(){
        sendChangementTitre(idPoste);
    });
}

function sendChangementTitre(idPoste)
{
    baliseMsgInModal = "msgInModalChangementTitrePoste";
    NewTitrePoste= document.getElementById("NouveauTitrePoste").value;
    mdpUser= document.getElementById("mdpChangementTitrePoste").value;
    idPoste = String(idPoste);

    if(isEmptyOrSpaces(mdpUser))
    {
        PrintMessage(baliseMsgInModal,"Le mots de passe est vide",true);
        return;
    }

    console.log(baliseMsgInModal);

    console.log(NewTitrePoste);

    console.log(mdpUser);

    console.log(idPoste);
}


function SuppressionPoste(idPoste,PseudoPosteur)
{
    document.getElementById("SupplemmentSuppressionPoste").innerHTML=PseudoPosteur;

    $("#modalSuppressionPoste").iziModal('open');

    document.getElementById("btnValideSuppressionPoste").addEventListener('click',function(){
        sendDeletePoste(idPoste);
    });
}


function sendDeletePoste(idPoste){

    baliseMsgInModal = "msgInModalSuppressionPoste";
    mdpUser = document.getElementById("mdpSuppressionPoste").value;

    if(isEmptyOrSpaces(mdpUser))
    {
        PrintMessage(baliseMsgInModal,"Le mots de passe est vide",true);
        return;
    }

    idPoste=String(idPoste);
    SendAjax("","Status du poste",baliseMsgInModal,idPoste,mdpUser);
}


function BanUser(idUserPoste,PseudoPosteur)
{

    $("#modalBan").iziModal({
        headerColor: '#00bfff',
        onOpening: ActiveBlockBackground,
        onClosing: disableBlockBackground,
    });

    document.getElementById("SupplemmentBan").innerHTML=PseudoPosteur;

    $("#modalBan").iziModal('open');

    document.getElementById("btnValideBan").addEventListener('click',function(){
        sendBanUser(idUserPoste);
    });
}
function sendBanUser(idUserPoste)
{
    baliseMsgInModal = "msgInModalBan";
    mdpUser = document.getElementById("mdpBan").value;

    if(isEmptyOrSpaces(mdpUser))
    {
        PrintMessage(baliseMsgInModal,"Le mots de passe est vide",true);
        return;
    }

    idUserPoste=String(idUserPoste);
    SendAjax("","Status du poste",baliseMsgInModal,idPoste,idUserPoste);
}