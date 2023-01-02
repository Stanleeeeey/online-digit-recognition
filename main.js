
brushSize = 2;

y = 0
x = 0
mouseDown = 0;


px = -1;
py = -1;

onload = function(e){ 

    mouseDown = 0;

    canva = document.getElementById('canva')
    c = canva.getBoundingClientRect()

    canva.width = Math.min(window.innerWidth, window.innerHeight*0.7);
    canva.height = Math.min(window.innerWidth, window.innerHeight*0.7);
}



window.onmousedown = function() { 
    mouseDown+=1;
  }
window.onmouseup = function() {
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

function saveImg(){
    canva = document.getElementById('canva')
    myImage  = canva.toDataURL("image/png"); 
    
    imageElement = document.getElementById("input");  
    imageElement.src = myImage;   

}
