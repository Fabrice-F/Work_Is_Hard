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