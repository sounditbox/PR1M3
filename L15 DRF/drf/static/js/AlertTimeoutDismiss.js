let messages = document.querySelectorAll('.alert');
for (let message of messages){
    setTimeout(() => message.remove(), 5000);
}
