document.querySelector('#searchIcon').addEventListener('click', show_search_field);
document.querySelector('#hideSearch').addEventListener('click', hide_search_field);


function show_search_field() {
    document.querySelector('#searchIcon').style.display = 'none'
    document.querySelector('#searchField').style.display = 'inline-flex'

}

function hide_search_field() {
    document.querySelector('#searchField').style.display = 'none'
    document.querySelector('#searchIcon').style.display = 'inline-flex'
}
