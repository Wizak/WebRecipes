var head = document.getElementById('head');
var down = document.getElementById('down');

window.addEventListener('scroll', function(e) {
  var scroll = window.pageYOffset || document.documentElement.scrollTop ||
                document.body.scrollTop || 0;
  head.style.opacity = Math.max(0, Math.min(1, -scroll / 400 + 2));
  if (head.style.opacity > 0) {
    head.style.display = "block";
  } else {
    head.style.display = "none";
  }
});
