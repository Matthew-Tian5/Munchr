var imageInput;
var foodImg;
/** @type { HTMLElement } */ var foodDrop;
var inputArea;
var inputText;
var submitButton;
var chatContainer;
var optionsSection;

function loaded() {
	imageInput = document.getElementById("imageInput");
	foodImg = document.getElementById("foodImg");
	foodDrop = document.getElementById("foodDrop");
	inputArea = document.getElementById("inputArea");
	inputText = document.getElementById("inputText");
	submitButton = document.getElementById("submitButton");
	chatContainer = document.getElementById("chatContainer");
	optionsSection = document.getElementById("optionsSection");

	// Handle image upload
	imageInput.addEventListener("change", e => {
		if (e.target.files && e.target.files[0]) {
			const reader = new FileReader();
			
			reader.onload = function(e) {
				foodImg.src = e.target.result;
				foodImg.style.display = "block";
				foodDrop.hidden = true;
				inputArea.removeAttribute("hidden")
				optionsSection.removeAttribute("hidden");
				
				// Add user message
				addMessage("I've uploaded an image of my food. What can you tell me about it?", false);
				
				// Simulate AI response
				sendRequest();
			};
			
			reader.readAsDataURL(e.target.files[0]);
		}
	});

	// Handle text submission
	submitButton.addEventListener("click", sendMessage);
	inputText.addEventListener("keypress", e => {
		if (e.key == "Enter" && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	});

	function sendMessage() {
		const message = inputText.value.trim();
		if (message) {
			addMessage(message, false);
			inputText.value = "";
			
			// Show loading indicator
			const loadingMessage = document.createElement("div");
			loadingMessage.className = "message ai-message";
			loadingMessage.innerHTML = "<div class=\"loading\"></div>";
			chatContainer.appendChild(loadingMessage);
			chatContainer.scrollTop = chatContainer.scrollHeight;
			
			// Simulate AI response
			sendRequest();
		}
	}

	function addMessage(text, isAI) {
		const messageDiv = document.createElement("div");
		messageDiv.className = `message ${isAI ? "ai" : "user"}-message`;
		messageDiv.textContent = text;
		chatContainer.appendChild(messageDiv);
		chatContainer.scrollTop = chatContainer.scrollHeight;
	}

	// Drag and drop functionality
	foodDrop.addEventListener("dragover", e => {
		e.preventDefault();
		foodDrop.classList.add("drag");
	});

	foodDrop.addEventListener("dragleave", () => {
		foodDrop.classList.remove("drag");
	});

	foodDrop.addEventListener("drop", e => {
		e.preventDefault();
		foodDrop.classList.remove("drag");
		
		if (e.dataTransfer.files && e.dataTransfer.files[0]) {
			imageInput.files = e.dataTransfer.files;
			const event = new Event("change", { bubbles: true });
			imageInput.dispatchEvent(event); // re-use change code
		}
	});
}