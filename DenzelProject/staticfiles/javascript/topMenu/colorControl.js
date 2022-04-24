export function colorize(color){
    let topMenu = document.querySelector('#topMenu');
    topMenu.querySelector('#logoutBtn').style.color = color;
    topMenu.querySelector('h1').style.color = color;
    topMenu.querySelector('#stripes').style.color = color
}
