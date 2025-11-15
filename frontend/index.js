/** @type { HTMLLabelElement } */ var drop;
/** @type { HTMLInputElement } */ var input;
/** @type { HTMLImageElement } */ var preview;

function loaded() {
	drop = document.getElementById("food-drop");
	input = document.getElementById("image-input");
	preview = document.getElementById("food-img");

	drop.addEventListener("drop", dropHandler);

	drop.addEventListener("dragover", ev => { // trigger hover effect
		let items = ev.dataTransfer.items;
		if (items.length == 1 && items[0].kind == "file" && items[0].type.startsWith("image/")) {
			ev.preventDefault();
			ev.dataTransfer.dropEffect = "copy";
			drop.classList.add("image_hover");
		} else {
			ev.dataTransfer.dropEffect = "none";
		}
	});

	drop.addEventListener("dragleave", () => { // remove hover effect
		drop.classList.remove("image_hover");
	})

	input.addEventListener("change", ev => {
		if (ev.target.files.length == 1 && ev.target.files[0].type.startsWith("image/"))
			displayPreview(ev.target.files[0]);
		else
			alert("Please upload only 1 image")
	});
}

/**
 * 
 * @param { File } file
 */
function displayPreview(file) {
	if (file.type.startsWith("image/")) {
		preview.src = URL.createObjectURL(file);
		preview.alt = file.name;
	} else {
		alert("You must upload a valid image");
	}
}

/**
 * 
 * @param { DragEvent } ev 
 */
function dropHandler(ev) {
	ev.preventDefault();
	drop.classList.remove("image_hover");
	if (ev.dataTransfer.items.length != 1) {
		alert("Please upload only 1 image");
		return;
	}
	let file = ev.dataTransfer.items[0];
	if (file.kind != "file" || !file.type.startsWith("image/")) {
		alert("You must upload a valid image");
		return;
	}
	displayPreview(file.getAsFile());
}