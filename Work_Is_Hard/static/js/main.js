function EnvoiFormulaireInscription(){

    var mdp = document.getElementById("mot_de_passe").value;
    var confirmation_mdp = document.getElementById("confirm_mdp").value;



    console.log(mdp);
    console.log(confirmation_mdp);

    if(mdp == confirmation_mdp){
        alert("Les deux mots de passe sont identiques.");
        return true;
    }else{
        alert("les mots de passe sont differents");
        return false;
    }
}
