const commentForm = document.getElementById('comment-form');
const commentBtn = document.getElementById("comment-btn");
const commentColumn = document.getElementById('comments-column');
const SENDURL = 'http://127.0.0.1:5000/comment/new/';
const DELETEURL = 'http://127.0.0.1:5000/comment/delete/';

function createAddClassElement(typeElement,classes){
	const newEl = document.createElement(typeElement);
	for(let i=0; i<classes.length ;i++){
		newEl.classList.add(classes[i]);
	}
	return newEl;
}

function renderComment(comment){
	const rowDiv = createAddClassElement('div',['row', 'justify-content-center'])
	const colDiv = createAddClassElement('div',['col-md-12']);
	const spanEl1 = createAddClassElement('span',[]);
	const spanEl2 = createAddClassElement('span',['font-weight-bold']);
	const smallEl = createAddClassElement('small',[]);
	const aNameEl = createAddClassElement('a',['text-dark']);
	const aDeleteEl = createAddClassElement('a',['text-danger', 'ml-2', 'delete-links']);

	const spanEl3 = createAddClassElement('span',['ml-1','font-weight-normal']);	
	spanEl3.textContent = comment.content;

	aNameEl.href = `/profile/${comment.username}`;
	aNameEl.textContent = comment.username;
	aDeleteEl.href = `#`;
	aDeleteEl.dataset.post_id = comment.post_id;
	aDeleteEl.dataset.comment_id = comment.comment_id;
	aDeleteEl.addEventListener('click',deleteComment);
	aDeleteEl.textContent = 'delete';

	spanEl2.appendChild(aNameEl);
	spanEl2.appendChild(spanEl3);

	smallEl.appendChild(aDeleteEl);
	spanEl2.appendChild(smallEl);

	spanEl1.appendChild(spanEl2);

	colDiv.appendChild(spanEl1);
	rowDiv.appendChild(colDiv);

	commentColumn.appendChild(rowDiv);
}

function sendComment(event){
	event.preventDefault();
	let postId= commentBtn.dataset.comment;
	let commentText = commentForm['comment-text'].value;

	const comment = {
		post_id: postId,
		comment: commentText
	};

	fetch(SENDURL,{
		method:'POST',
		body:JSON.stringify(comment),
		headers:{
			'Content-type': 'application/json; charset=UTF-8'
		}
	})
	.then(response => response.json())
	.then(output =>{
		if(output.is_done){
			renderComment(output);
			commentForm['comment-text'].value = '';
		}else{
			alert("Something went Wrong unable to handle comment ");
		}
	});
}


function deleteComment(event){
	event.preventDefault();
	const deleteTag = event.target;
	let postId = deleteTag.dataset.post_id;
	let commentId = deleteTag.dataset.comment_id;
		
	const comment = {
		post_id: postId,
		comment_id: commentId
	};
	// console.log(comment);
	fetch(DELETEURL,{
		method:'POST',
		body:JSON.stringify(comment),
		headers:{
			'Content-type': 'application/json; charset=UTF-8'
		}
	})
	.then(response => response.json())
	.then(output =>{
		if(output.is_done){
			// console.log(output);
			deleteTag.parentNode.parentNode.parentNode.parentNode.remove();
		}else{
			alert("Something went Wrong unable to handle comment ");
		}
	});
}


commentForm.addEventListener('submit',sendComment);

const deleteLinks = document.getElementsByClassName('delete-links');
for(let i=0; i<deleteLinks.length; i++){
	deleteLinks[i].addEventListener('click',deleteComment)
}
