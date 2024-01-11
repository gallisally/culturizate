document.addEventListener("DOMContentLoaded",function(){
    const form=document.getElementById("question-form");

    console.log("add event litener funciona");
    if (form){
        form.addEventListener('submit',function(event){
        //evitar recarga automatica de la pagina al enviar el formulario
        //event.preventDefault();
        sendResponse();

        });
        console.log('La funcion ha funcionado correctamente');

    }else{
        console.error('El formulario no se ha enviado correctamente');
    }   
});
function sendResponse(){
    //event.preventDefault(); 
    //obtener formulario
    console.log("ejecutando js")
    const form= document.getElementById("question-form");
    //creacion objeto fromData para obtener pares clave-valor
    const formData= new FormData(form);
    // enviar solicitud post para enviar datos
    fetch(form.action,{
        method:'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor', data)
        seeResponse(data),
        newQuestion()
    })
    .catch(error=>console.error('Error', error));

}

function seeResponse(data){
    // obtener contenedor actual
    const responseContainer=document.getElementById("response-container")
    // actualizar el contenido del contenedor. El servidor devuelve el contenido de la propiedad mensaje del objeto data
    responseContainer.innerHTML=  `<p>${data.mensaje}</p>`

}

function newQuestion(url){
    //obtener nueva pregunta con solicitud get
    fetch(url)
    .then(response=> response.json())
    .then(data => {
        if (data.question){
            updateContent(data.question);
        }
    })
    .catch(error =>console.log ('Error', error));
}

function updateContent(){
    //seleccion de elementos del html
    const questionText=document.querySelector('#game-container h3');
    const questionOptions= document.querySelector('#game-container p');
    const difficulty =document.querySelector('#game-container p:nth-last-child(3)');
    const category= document.querySelector('#game-container p:nth-last-child(2)');
    const points=document.querySelector('#game-container p:nth-last-child');
    //actualizacion elementos html
    questionText.textContent=question.question_text;
    questionOptions.textContent=question.options;
    difficulty.textContent=question.nivel_dificultad;
    category.textContent=question.category;
    points.textContent=question.points;
    // nivelDificultad.textContent = `Nivel de Dificultad: ${pregunta.nivel_dificultad}`;



}