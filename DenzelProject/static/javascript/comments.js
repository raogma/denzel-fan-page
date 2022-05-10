import {sendRequest} from './requestControl.js';
import { loadPagination } from './paginationTemplate.js';
import { loadDialogBox } from './dialogBox.js';
import { hideDialogBox } from './dialogBox.js';
import { loadComment } from './commentTemplate.js';

const postPk = window.location.pathname.split('/')[3];
const user = document.querySelector('#user').value;
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

const dialogBox = document.querySelector('#deleteDialogBox');
const commentsContainer = document.querySelector('#commentsContainer');
const commentsPagination = document.querySelector('#comment-pagination-container');
const url = `/posts/details/${postPk}/commentsREST/`;
const overlay = document.querySelector("#notMyOverlay");
const commentButton = document.querySelector('#showComments');
const commentsGlobal = document.querySelector('#comments');

let commentsData = {
    //position: div
}


overlay.addEventListener('click', ev => {
    hideDialogBox('any');
})

await loadComments(url);


commentButton.addEventListener('click', ev => {
    commentsGlobal.style.display === 'none' ?
        commentsGlobal.style.display = 'block' :
        commentsGlobal.style.display = 'none'
})

commentsPagination.addEventListener('click', (ev) => {
    if(ev.target.tagName == 'BUTTON'){loadComments(ev.target.id);}
});

commentsContainer.addEventListener('click', (ev) => commentListener(ev));
document.querySelector('#newCommentForm').addEventListener('submit', createCommentListener);


async function loadComments(url){
    let comments = await sendRequest(url, 'GET', undefined, csrf_token);
    let res = ''
    comments.results.map((x, i) => {
        res += `<div class="w3-container" id="commentContainer-${i}">`
        res += loadComment(x, user);
        res += '</div>'
    })
    commentsContainer.innerHTML = res;
    commentsPagination.innerHTML = loadPagination(comments.previous, comments.next);
}

function commentListener(ev) {
    const target = ev.target;
    if(target.tagName == 'BUTTON'){
        if (target.innerHTML === 'Edit'){
            const commentId = target.parentElement.id.split('-')[2];
            let commentContainer = target.parentElement.parentElement.parentElement;
            let cloneComment = commentContainer.cloneNode(true);
            commentsData[cloneComment.id.split('-')[1]] = cloneComment;
            const content = commentContainer.querySelector('p');
            const editForm = `
            <form method="POST" style="display:flex; flex-direction: row;" id="editCommentForm-${commentId}">
                <input placeholder="Edit Comment" value="${content.innerHTML}" class="w3-input w3-border-0" type="text">
                <button class="w3-button w3-padding" type="submit">Submit</button>
                <button class="w3-button w3-padding" type="reset">Cancel</button>
            </form>
            <hr>`

            commentContainer.innerHTML = editForm;
            commentsContainer.addEventListener('click', editCommentListener);

        }
        else if (target.innerHTML === 'Delete'){
            loadDialogBox('#deleteDialogBox');
            let commentId = ev.target.parentElement.id.split('-')[2];
            document.getElementById("deleteDialogBox").querySelector('button[value="delete"]').id = 'delCommentBtn-' + commentId;
            dialogBox.addEventListener('click', deleteCommentListener)
        }
    }
}


async function createCommentListener(ev){
    ev.preventDefault();
    if (user === 'None'){
        loadDialogBox('#authDialogBox');
        return;
    }
    let content = ev.target.querySelector('input').value;
    const body = {
        content,
        owner: user,
        post: postPk,
    }
    await sendRequest(url, 'POST', body, csrf_token);
    await loadComments(url);
    ev.target.reset();
}

async function editCommentListener(ev){
    ev.preventDefault();
    if (user === 'None'){
        loadDialogBox('#authDialogBox');
        return;
    }
    if (ev.target.tagName === 'BUTTON'){
        let btnName = ev.target.innerHTML.trim();
        if(btnName === 'Cancel') {
            let currentContainer = ev.target.parentElement.parentElement;
            currentContainer.innerHTML = commentsData[currentContainer.id.split('-')[1]].innerHTML;
        } else if (btnName === 'Submit') {
            const body = {
                content: ev.target.parentElement.querySelector('input').value,
                owner: user,
                post: postPk,
            }
            await sendRequest(url + ev.target.parentElement.id.split('-')[1] + '/', 'PUT', body, csrf_token);
            await loadComments(url);
        }
    }
}

async function deleteCommentListener(ev){
    if (ev.target.tagName === 'BUTTON'){
        let btnName = ev.target.innerHTML.trim();
        if(btnName === 'Cancel') {
            hideDialogBox('#deleteDialogBox');
        } else if (btnName === 'Delete') {
            await sendRequest(url + ev.target.id.split('-')[1] + '/', 'DELETE', undefined, csrf_token);
            await loadComments(url);
            hideDialogBox('#deleteDialogBox');
        }
    }
}
