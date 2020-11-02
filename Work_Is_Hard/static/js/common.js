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
