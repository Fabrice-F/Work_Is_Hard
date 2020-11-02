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

function isEmptyOrSpaces(str){
    if(str==undefined)
        return true;
    return str === null || str.match(/^ *$/) !== null;
}


function SendAjax(url,textSuccess,baliseMessage,...value)
{
    datas ="";

    for (let i = 0; i < value.length; i++) {
        variableName=  getVariableName(value[i])
        datas = `${datas}${variableName}=${value[i]}` ; 
        if(i+1!=value.length)
            datas +="&"
    }
    
    $.ajax({
        url : url, // La ressource ciblée
        type : 'POST', // Le type de la requête HTTP.
        data : datas ,
        dataType : 'text', // On désire recevoir du text
        success : function(text, statut){ // contient le text renvoyé
        if (text=="True"){
            PrintMessage(baliseMessage,`Le ${textSuccess} a été actualisé, rechargement de la page dans 2 secondes...`);
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

function getVariableName(v) {
    for (var key in window) {
        if (window[key] === v)
            return key;
    }
}