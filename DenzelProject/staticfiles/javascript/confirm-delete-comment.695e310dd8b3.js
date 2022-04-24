let dialog = constructBox();
let delBtns = Array.from(document.querySelectorAll('.delBtn'));
let overlay = document.querySelector('#myOverlay')
delBtns.map(x => x.addEventListener('click', ev => showBox(ev)));

function constructBox() {
    return `<div style="display:fixed; z-index:5" class="w3-display-middle pstForm" id="dialogBox">
    <h1 style="color:white">Are you sure you want to delete this comment?</h1>
    <div style="margin-left: 29%;">
        <button style="display:inline-flex" class="w3-button w3-section w3-blue-grey w3-ripple" id="delCommentBtn">Delete</a">
        <button style="display:inline-flex" class="w3-button w3-section w3-blue-grey w3-ripple" id="cancelCommentBtn">Cancel</button>
    </div>
</div>`
}

function showBox(ev){
    let csrftoken = document.querySelector('form input[name="csrfmiddlewaretoken"]').value
    postPk = ev.target.id.split('-')[1];
    commentPk = ev.target.id.split('-')[2];
    document.getElementById("myOverlay").style.display = "block";
    document.body.innerHTML += dialog

    let cancelBtn = document.querySelector('#cancelCommentBtn')
    if (cancelBtn) {
        cancelBtn.addEventListener('click', ev => {
            document.querySelector('#dialogBox').remove();
            document.getElementById("myOverlay").style.display = "none";
            Array.from(document.querySelectorAll('.delBtn')).map(x => x.addEventListener('click', ev => showBox(ev)));
        })
    }

    
    let deleteBtn = document.querySelector('#delCommentBtn')
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async function(ev) {
            let response = await fetch(`delete/${commentPk}/`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                }, 
                body: {}
            })
            location.reload();
        })
    }
}
