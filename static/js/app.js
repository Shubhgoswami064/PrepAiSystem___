let questions=[],i=0,score=0,timer,sec=15;

function startQuiz(){
 fetch("/start_quiz",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
    subject:document.getElementById("subject").value,
    difficulty:document.getElementById("difficulty").value,
    num:document.getElementById("num").value,
    timer:document.getElementById("timer").value
  })
 }).then(()=>location="/quiz");
}

window.onload=()=>{
 if(location.pathname=="/quiz"){
  fetch("/api/questions")
  .then(r=>r.json())
  .then(data=>{
    questions=data;
    document.getElementById("loading").style.display="none";
    document.getElementById("quiz").style.display="block";
    show();
  });
 }
}

function show(){
 let q=questions[i];

 document.getElementById("qCount").innerText=`Q ${i+1}/${questions.length}`;
 document.getElementById("score").innerText=`Score:${score}`;
 document.getElementById("question").innerText=q.question;

 let html="";
 q.options.forEach(o=>{
  html+=`<button onclick="select(this,'${o}')">${o}</button>`;
 });

 document.getElementById("options").innerHTML=html;
 startTimer();
}

function startTimer(){
 sec=15;
 timer=setInterval(()=>{
  document.getElementById("timerBox").innerText="⏱ "+sec;
  sec--;
  if(sec<0){clearInterval(timer);nextQ();}
 },1000);
}

function select(btn,opt){
 clearInterval(timer);

 let q=questions[i];

 if(opt==q.answer){
  btn.classList.add("correct");
  score++;
 }else{
  btn.classList.add("wrong");
 }

 document.getElementById("nextBtn").disabled=false;
}

function nextQ(){
 i++;
 if(i<questions.length) show();
 else showResult();
}

function showResult(){
 let msg = score > questions.length*0.7 ? "Strong" : "Weak";

 document.getElementById("resultModal").style.display="block";
 document.getElementById("finalScore").innerText=`Score: ${score}/${questions.length}`;
 document.getElementById("analysis").innerText=msg;
}

function goDashboard(){location="/dashboard"}

function logout(){fetch("/logout").then(()=>location="/")}