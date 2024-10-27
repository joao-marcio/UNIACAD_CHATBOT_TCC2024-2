// old
function sendData() { 
    document.getElementById('output').innerHTML = "PENSANO...";
    var value = document.getElementById('input').value; 
    $.ajax({ 
        url: '/process', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'value': value }), 
        success: function(response) { 
            document.getElementById('output').innerHTML = response.result; 
        }, 
        error: function(error) { 
            document.getElementById('output').innerHTML = "NÃO ENTENDI";
            console.log(error); 
        } 
    }); 
};
// new
function openForm() {
  document.getElementById("chat-popup").style.display = "block";
};
function closeForm() {
  document.getElementById("chat-popup").style.display = "none";
};
function sendMessage() {
    var message = document.getElementById("input").value;
    if (message !== "") {
        document.getElementById("typing-bubble").style.display = "flex";
        var userMessage = document.createElement("div");
        userMessage.classList.add("chat-message", "user-message");
        userMessage.textContent = message;
        document.querySelector(".chat-messages").appendChild(userMessage);
        let element = document.getElementsByClassName("chat-messages")[0];
        element.scrollTop = element.scrollHeight;
        $.ajax({
            url: 'localhost:5000/process',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'value': message }),
            success: function(response) {
                document.getElementById("typing-bubble").style.display = "none";
                displayReponseText(response.result);
            },
            error: function(error) {
                document.getElementById("typing-bubble").style.display = "none";
                console.log(error);
                var errorMessage = document.createElement("div");
                errorMessage.classList.add("chat-message", "bot-message");
                errorMessage.textContent = "Erro: Não consegui obter uma resposta.";
                document.querySelector(".chat-messages").appendChild(errorMessage);
                let element = document.getElementsByClassName("chat-messages")[0];
                element.scrollTop = element.scrollHeight;
            }
        });
        document.getElementById("input").value = "";
    }
};
function displayReponseText(text) {
    let i = 0;
    let lines = text.split('\n').filter(e => e);
    let callback = function() {
        if (i < lines.length) {
            displayParagraph(lines[i]);
            i = i + 1;
            setTimeout(callback, '1000');
        }   
    }
    callback();
};
function displayParagraph(text) {
    var botMessage = document.createElement("div");
    botMessage.classList.add("chat-message", "bot-message");
    botMessage.textContent = text;
    document.querySelector(".chat-messages").appendChild(botMessage);
    document.querySelector(".chat-messages").scrollTop = document.querySelector(".chat-messages").scrollHeight;
};
document.getElementById("input").addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter" || event.key === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        sendMessage();
    }
});