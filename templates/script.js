function back() {
    window.history.go(-1);
}
document.getElementById("postRec").addEventListener('submit',postData)

function postData(e) {
    e.preventDefault()

    let reg = parseInt(document.getElementById('reg').value)
    let name = document.getElementById('name').value  
   
    fetch(`http://localhost:5000/postData`, {
        method:'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({
            'reg': reg,
            'name': name
        })
    })
    .then((response)=> response.json())
    .then((data => console.log(data)))
}

document.getElementById("removeRec").addEventListener('submit',deleteRec)

function deleteRec(e){
    e.preventDefault()

    let reg = document.getElementById('regno').value
    fetch(`http://localhost:5000/deleteRec/${reg}`,{method:'DELETE'})
    .then((res)=>res.json())
    .then((res=>console.log(res)))
    // then((res=> document.getElementById('delResponse').innerHTML = `Deleted`))
}


document.getElementById("loginData").addEventListener('submit',loginRec)

function loginRec(e){
// $("form[name=loginData").submit(function(e){
    e.preventDefault()

    let uid = document.getElementById('username').value
    let pass = document.getElementById('password').value
    
    fetch(`http://localhost:5000/check/${uid}&${pass}`,{method:'GET'}
    //     , {method:'POST',
    //     headers : {
    //         'Content-Type' : 'application/json'
    //     },
    //     body : JSON.stringify({
    //         'uid': uid,
    //         'pass': pass
    //     })    }
    )
    .then((res)=>res.json())
    .then((res=>console.log(res))) 
}
// $("form[name=loginData").submit(function(e){

// })