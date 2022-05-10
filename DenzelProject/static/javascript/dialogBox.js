export function loadDialogBox(targetBox) {
    document.querySelector("#notMyOverlay").style.display = "block";
    document.querySelector(targetBox).style.display = "block";
}

export function hideDialogBox(targetBox) {
    document.querySelector("#notMyOverlay").style.display = "none";
    if (targetBox === 'any'){
        Array.from(document.querySelectorAll('.pstForm'))
            .map(x => x.style.display = "none")
        return;
    }
    document.querySelector(targetBox).style.display = "none";
}

