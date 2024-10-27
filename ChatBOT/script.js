function sendMessage() {
  var message = document.getElementById("input").value;
  if (message !== "") {
      var userMessage = document.createElement("div");
      userMessage.classList.add("chat-message", "user-message");
      userMessage.textContent = message;
      document.querySelector(".chat-messages").appendChild(userMessage);

      
      $.ajax({
          url: '/process',
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({ 'value': message }),
          success: function(response) {
             
              var botMessage = document.createElement("div");
              botMessage.classList.add("chat-message", "bot-message");
              botMessage.textContent = response.result;
              document.querySelector(".chat-messages").appendChild(botMessage);

              
              document.querySelector(".chat-messages").scrollTop = document.querySelector(".chat-messages").scrollHeight;
          },
          error: function(error) {
              console.log(error);
              
              var errorMessage = document.createElement("div");
              errorMessage.classList.add("chat-message", "bot-message");
              errorMessage.textContent = "Erro: Não consegui obter uma resposta.";
              document.querySelector(".chat-messages").appendChild(errorMessage);
          }
      });
      document.getElementById("input").value = "";
  }
}