export function loadPagination(previous, next){
    let pageNum = 1;

    if (next){
        pageNum = Number(next.split('?')[1].split('=')[1]) - 1;
    }
    
    let res = `<div  class="w3-bar">`;
    if (previous){
        const temp = previous.split('?')[1];
        if(temp){
            pageNum = Number(temp.split('=')[1]) + 1;
        }
        res += `<button id="${previous}" class="w3-bar-item w3-button w3-hover-black">«</button>`
    }

    res += `<span class="w3-bar-item w3-black">${pageNum}</span>`

    if (next){
        res += `<button id="${next}" class="w3-bar-item w3-button w3-hover-black">»</button>`
    }

    res += `</div>`
    return res;
}