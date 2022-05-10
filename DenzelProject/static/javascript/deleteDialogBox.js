export function loadDialogBox(commentId) {
    document.getElementById("myOverlay").style.display = "block";
    document.getElementById("dialogBox").style.display = "block";
    document.getElementById("dialogBox").querySelector('button[value="delete"]').id = 'delCommentBtn-' + commentId;
}

export function hideDialogBox() {
    document.getElementById("myOverlay").style.display = "none";
    document.getElementById("dialogBox").style.display = "none";
}
