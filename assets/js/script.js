let popup = document.getElementById('mypopup');

document.body.onclick = (event) => {
    const elem = event.target;
    if (elem.classList.contains('form-control')) {
        navigator.clipboard.writeText(elem.value)
        popup.style.display='block'
        setTimeout(() => popup.style.display='none', 1500)
    }
}