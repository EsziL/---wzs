document.addEventListener('DOMContentLoaded', main);

function main() {
  
  
  
}


function getTop(el) {
	return el.getBoundingClientRect().top + window.scrollY;
}



function setTop(el, desiredTop) {
  el.style.top = desiredTop - getTop(el) + 'px';
}

