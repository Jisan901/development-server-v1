document.getElementById('searchB').onkeyup = function(e){
    if (e.key === "Enter"){
        let s = e.target.value.toLowerCase();
        location.pathname='/blogs/search/'+s+'/1'
    }
}
function dangerAlert(massage,time=4000) {
    if(massage.length>0){const danger = document.createElement('div');
    danger.classList.add('alert-danger');
    danger.innerText=massage;
    document.body.appendChild(danger);
    const tm2 = setTimeout(()=>{
            danger.classList.add('alert-show');
            clearTimeout(tm2)
        },500);
    
    const timeout = setTimeout(function() {
        danger.classList.add('danger-hide');
        const tm3 = setTimeout(()=>{
            document.body.removeChild(danger);
            clearTimeout(tm3)
        },500);
        clearTimeout(timeout)
    }, time);}
}
function rateus(){
        let box = document.createElement('div')
        box.innerHTML=`
    <div class="rate-course-overlay"></div>
    <div class="rate-course flex-center">
    <input type="hidden" name="ratedata" id="ratedata" value="1" />

        <h3>rate this course</h3>
        
        <div class="stars">
            <ion-icon name="star" data-rate="1" class=" inp"></ion-icon>
            <ion-icon name="star" data-rate="2" class="off inp"></ion-icon>
            <ion-icon name="star" data-rate="3" class="off inp"></ion-icon>
            <ion-icon name="star" data-rate="4" class="off inp"></ion-icon>
            <ion-icon name="star" data-rate="5" class="off inp"></ion-icon>
        </div>
        <button class="danger" id="rated">ok</button>
    </div>
`
        document.body.appendChild(box);
        setTimeout(function() {
                    document.querySelectorAll(".inp").forEach((d)=>{
        d.addEventListener("click",(e)=>{
            let targetrate = e.target.getAttribute('data-rate');
            document.getElementById('ratedata').value=targetrate;

            for (let i = 1; i <= 5; i++) {
                let m = document.querySelector(".inp[data-rate=\""+i+"\"]")
                m.classList.remove('off')
                if (i>targetrate) {
                    m.classList.add('off')
                }
            }
            
        })
        })

        document.querySelector('.rate-course-overlay').onclick=(e)=>{
            document.body.removeChild(box);
            e.stopPropagation();
        }
        document.getElementById('rated').onclick=()=>{
            let value=document.getElementById('ratedata').value
            console.log('hello',value);
        }
        }, 1000);
    }
    
    window.addEventListener("pageshow", function (event) {
        var historyTraversal = event.persisted ||
        (typeof window.performance != "undefined" &&
            window.performance.navigation.type === 2);
        if (historyTraversal) {
            // Handle page restore.
            window.location.reload();
        }
    });
        document.querySelectorAll('.rating-star').forEach((e)=>{
            let v = parseInt(e.getAttribute('-data-rating'))
            for (let i = 1; i <= 5; i++) {
                if (i<=v) {
                e.innerHTML += '<ion-icon name="star"></ion-icon>'
                }
                else{
                    e.innerHTML += '<ion-icon name="star" class="off"></ion-icon>'
                }
            }
        })
        
        
if(!document.getElementById('web_jumpers')){   

let jumpers = document.querySelectorAll("a");
jumpers.forEach(jumper => {
        jumper.onclick = function(event) {
            var e = event || window.event ;
            if(e.preventDefault) {
                e.preventDefault();
            } else {
                e.returnValue = true ;
            }
            location.replace(this.href);
            jumper = null;
        }
})}




document.getElementById('searchC').onkeyup = function(e){
    if (e.key === "Enter"){
        let s = e.target.value.toLowerCase();
        location.pathname='/courses/search/'+s.toLowerCase()
    }
}
