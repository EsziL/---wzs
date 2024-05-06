document.addEventListener('DOMContentLoaded', main);

function main() {
  const login = document.getElementById("login");
  const iframe = document.getElementById("loginiframe");
  let logindiv;

  iframe.addEventListener("load", ()=>{
    logindiv = iframe.contentWindow.document.getElementById("login");
    const loginclose = iframe.contentWindow.document.getElementById("loginclose");
    loginclose.addEventListener("click", ()=>{
      logindiv.style.opacity = "0%";
      // iframe.style.opacity = "0%";
      setTimeout(()=>{
        iframe.style.visibility = "hidden";
      }, 250);
    });
  });
  login.addEventListener("click", ()=>{
    iframe.style.visibility = "visible";
    // iframe.style.opacity = "100%";
    logindiv.style.opacity = "100%";
  });

  const spans = document.querySelectorAll("span");
  spans.forEach((i)=>{
    i.addEventListener("click", ()=>{
      window.location.href = i.getAttribute("href");
    });
  })
}


function getTop(el) {
	return el.getBoundingClientRect().top + window.scrollY;
}



function setTop(el, desiredTop) {
  el.style.top = desiredTop - getTop(el) + 'px';
}

