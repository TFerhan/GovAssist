const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message// Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined"><img src="trbch.png"></span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = message;
    return chatLi; // return chat <li> element
}

const generateResponse = (chatElement) => {
    const API_URL = "https://dgov-7e66641fcc9a.herokuapp.com/api";
    const messageElement = chatElement.querySelector("p");
    const payload = {
        message: messageElement.textContent,
    };

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    };

    fetch(API_URL, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const message = data;
            const links = extractLinks(message);
            const formattedMessage = formatMessageWithLinks(message, links);
            const incomingChatLi = createChatLi(formattedMessage, "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
        })
        .catch(error => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again.";
            console.error('There was a problem with the fetch operation:', error);
        })
        .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    outcom = createChatLi(userMessage, "outgoing")
    chatbox.appendChild(outcom);
    chatbox.scrollTo(0, chatbox.scrollHeight);

    generateResponse(outcom);

}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

const extractLinks = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.match(urlRegex);
}

// Function to format a message with clickable links
const formatMessageWithLinks = (message, links) => {
    if (!links) {
        return message;
    }
    let formattedMessage = message;
    links.forEach(link => {
        formattedMessage = formattedMessage.replace(link, `<a href="${link}" target="_blank">Lien</a>`);
    });
    return formattedMessage;
}

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

