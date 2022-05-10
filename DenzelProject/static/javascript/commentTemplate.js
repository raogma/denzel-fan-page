export function loadComment(commentObj, user){
    let res = '';
    if (commentObj.owner == user){
        res += `
    <div style="float:right" class="w3-dropdown-hover">
        <button class="w3-button w3-ripple w3-white">&#8285;</button>
        <div id="comment-control-${commentObj.id}" class="w3-dropdown-content w3-bar-block w3-border">
            <button class="w3-bar-item w3-button editBtn">Edit</button>
            <button class="w3-bar-item w3-button delBtn">Delete</button>
        </div>
    </div>`
    }
    res += `
    <h6 style="display: inline-block;" class="w3-text-teal"><i
            class="fa fa-calendar fa-fw w3-margin-right"></i>${commentObj.created}</h6>
    <div class="contentComment">
        <p>${commentObj.content}</p>
    </div>
    <hr>`
    return res;
}