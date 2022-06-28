function myFunction() {
    document.querySelector('#outer_form')?.addEventListener('submit', (e) => {
        e.preventDefault()
        const id = e.target.id.value
        fetch('https://reqres.in/api/users/' +id).then(
            response => response.json()
        ).then(
            response => createUsersList(response.data)
        ).catch(
            err => console.log(err)
        );
    })
}

function createUsersList(response) {
        console.log(response.data)

    const currMain=document.querySelector("form")

    const section = document.getElementById('frontend_section')
    section.innerHTML = `
        <h3>Full Name: ${response.first_name} ${response.last_name} </h3>
        <h3>Email: ${response.email} </h3>
       <img src="${response.avatar}" alt="The Avatar">
    
    `
    currMain.appendChild(section)

}