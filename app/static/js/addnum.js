
brushSize = 2;

y = 0
x = 0
mouseDown = 0;


px = -1;
py = -1;



onload = function(e){ 


    mouseDown = 0;

    const select = document.getElementById('value');
    canva = document.getElementById('canva')

    select.addEventListener('change', (event) => {
        e.preventDefault()
        // disable the select element while drawing
        if (event.target !== canva) {
          select.disabled = mouseDown;
        }
      });


    c = canva.getBoundingClientRect()

    canva.width = Math.min(window.innerWidth, window.innerHeight*0.7);
    canva.height = Math.min(window.innerWidth, window.innerHeight*0.7);
}



window.onmousedown = function(e) {
    
    const select = document.getElementById('value');
    canva = document.getElementById('canva')
    if (event.target === canva) {
        select.disabled = true;
        
    }else if(event.target = select){
        select.size = 10
    }
    
    mouseDown+=1;
  }
window.onmouseup = function(e) {
    e.preventDefault()
    const select = document.getElementById('value');
    select.disabled = false;
    mouseDown-=1;
    px = -1;
    py = -1
  }

window.onmousemove = (e) => {
    canva = document.getElementById('canva')
    c = canva.getBoundingClientRect()



    x = e.clientX;
    y  = e.clientY;


    if (canva.getContext && mouseDown === 1) {
        const ctx = canva.getContext("2d");

        if(px !== -1){
            ctx.beginPath();
            ctx.lineWidth = 5;
            ctx.moveTo(px-c.left, py-c.top);
            ctx.lineTo(x-c.left, y-c.top);
            ctx.stroke();
            

            px = x;
            py = y;
        }else{
            px =x;
            py = y;
        }
    }
}

function startanimation(){
    document.getElementById('canva').style.display = 'none'
    document.getElementById('loading').style.display = "block"
}

function stopanimation(ans){
    document.getElementById('loading').style.display = 'none'
    document.getElementById('ans').style.display = "block"
    document.getElementById('ans').innerHTML = ans
    
    document.getElementById('button').innerHTML = "draw next"
    document.getElementById('button').onclick = () => {location.reload()}
}

async function saveImg(){
    document.getElementById('value').size = 1;

    canva = document.getElementById('canva')
    myImage  = canva.toDataURL("image/png"); 
    


    startanimation();



    value = document.getElementById('value').value;
    console.log(value)
    response = await fetch('/addnum', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "image":myImage,
        "value":value
    })
    })
    .then((response) => response.json())
    .then((data) => {

      ans = data
    })

    stopanimation("succes");





}
