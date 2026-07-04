window.onload = () => {
  document.querySelectorAll(".card").forEach((c, i) => {
    setTimeout(() => {
      c.classList.add("fade-in");
    }, i * 100);
  });
};