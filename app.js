const chatOutput = document.getElementById('chat-output');
const chatInput = document.getElementById('chat-input');

function sendChat() {
  const userText = chatInput.value;
  chatOutput.innerHTML += `<p>You: ${userText}</p>`;
  chatInput.value = '';

  // send userText to server and get response
  fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: userText })
  })
  .then(response => response.json())
  .then(data => {
    chatOutput.innerHTML += `<p>ChatGPT: ${data.text}</p>`;
  });
}

chatInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    sendChat();
  }
});