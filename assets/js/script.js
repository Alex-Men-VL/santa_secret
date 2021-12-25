document.body.onclick = (event) => {
    const elem = event.target;
    if (elem.classList.contains('form-control')) {
        navigator.clipboard.writeText(elem.value)
        console.log(elem)
        successMessage.classList.add('active')
        setTimeout(() => successMessage.classList.remove('active'), 2000)
    }
}