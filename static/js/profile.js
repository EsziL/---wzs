document.addEventListener("DOMContentLoaded", () => {
  main();
});

function main() {
  parse();
}

function parse() {
  const parse = document.querySelectorAll(".parse");

  fetch("/userdata")
    .then((response) => {
        if (response.status === 401) {
            window.location.href = '/login';
            throw new Error("Unauthorized");
        }
      return response.json();
    })
    .then((data) => {
      parse.forEach((i) => {
        i.innerHTML = i.innerHTML.replace("!{user}", data.username);
      });
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });

}
