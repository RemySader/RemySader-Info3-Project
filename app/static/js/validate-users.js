const checkIfUserExists = (e) => {
    const emailFormElement = e.target
    const email = e.target.value
    axios.post('/validate-users', {
        email: email
    })
    .then((response) => {
        if(response.data.user_exists == "true") {
            emailFormElement.setCustomValidity("This user already exists, please login instead.")
            emailFormElement.reportValidity()
        }
    }, (error) => {
        console.log(error)
    })
}