
var mybutton = document.getElementById("myBtn");
mybutton.addEventListener('click',()=>{
	document.body.scrollTop = 0;
	document.documentElement.scrollTop = 0;
});
// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
