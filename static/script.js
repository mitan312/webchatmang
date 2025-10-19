const socket = io();

const msgBox = document.getElementById('messages');
const input = document.getElementById('message');
const sendBtn = document.getElementById('send');

sendBtn.onclick = () => {
  const msg = input.value.trim();
  if (msg) {
    socket.send(msg);
    input.value = '';
  }
};

socket.on('message', (msg) => {
  const div = document.createElement('div');
  div.textContent = msg;
  div.classList.add('p-2', 'my-1', 'bg-gray-700', 'rounded-lg');
  msgBox.appendChild(div);
  msgBox.scrollTop = msgBox.scrollHeight;
});
