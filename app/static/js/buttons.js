

function setBC(){
    elem = document.getElementById('div_sq')
    op = elem.style.opacity
    if (op == '0.2')
        elem.style.opacity = '0.7';
    else
        elem.style.opacity = '0.2';

}

function show_main(){
    document.getElementById('page_main').style.display = "block"
    document.getElementById('page_about1').style.display = "none"
    document.getElementById('page_about2').style.display = "none"
    document.getElementById('page_contacts').style.display = "none"
}

function show_about1(){
    document.getElementById('page_main').style.display = "none"
    document.getElementById('page_about1').style.display = "block"
    document.getElementById('page_about2').style.display = "none"
    document.getElementById('page_contacts').style.display = "none"
}

function show_about2(){
    document.getElementById('page_main').style.display = "none"
    document.getElementById('page_about1').style.display = "none"
    document.getElementById('page_about2').style.display = "block"
    document.getElementById('page_contacts').style.display = "none"
}

function show_contacts(){
    document.getElementById('page_main').style.display = "none"
    document.getElementById('page_about1').style.display = "none"
    document.getElementById('page_about2').style.display = "none"
    document.getElementById('page_contacts').style.display = "block"
}
