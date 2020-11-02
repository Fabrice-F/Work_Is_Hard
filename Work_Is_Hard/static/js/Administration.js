/* Role */

new CBPFWTabs( document.getElementById( 'tabs' ) );

$("#modal_changeRole").iziModal({
    closeButton: true,
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
    document.location.reload();
}

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

    console.log(idUser)
    console.log(pseudo)
    console.log(ancienRole)
    console.log(NouveauRole)
    console.log("==================")


}

function ValidChangeRole(pseudo,id,ancienRole,NouveauRole)
{
    AdminPwd = document.getElementById("mdpChangeRole").value
    baliseMessage ="msgInchangeRole";
    
    if(AdminPwd=="")
    {
        PrintMessage(baliseMessage,"Le champs mot de passe est vide",true);
        return
    }

    $.ajax({
        url : '/ChangementRole', // La ressource ciblée
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