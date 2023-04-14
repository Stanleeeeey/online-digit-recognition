
async function Remove(id, label){
    response = await fetch('/delete', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "id":id,
            "label" : label
        })
        })
        .then((response) => response.json())
        .then((data) => {
    
          ans = data
        })

        location.reload()
    
}