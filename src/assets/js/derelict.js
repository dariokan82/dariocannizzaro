/* The two derelict touches on the front page. Progressive: the page is
   complete without this file (strip 01 shows, the counter reads ------). */
(function () {
  var strip = document.querySelector("[data-strips]");
  if (strip) {
    try {
      var list = JSON.parse(strip.getAttribute("data-strips"));
      if (list.length > 1) strip.src = list[Math.floor(Math.random() * list.length)];
    } catch (e) {}
  }

  var odo = document.querySelector("[data-counter]");
  if (odo && window.fetch) {
    // Abacus: a free, keyless hit counter with CORS. `hit` increments and returns
    // { value }. If it ever dies, the dashes stay and nothing else breaks.
    fetch("https://abacus.jasoncameron.dev/hit/" + odo.getAttribute("data-counter"))
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var n = String(j.value || 0);
        var cells = odo.querySelectorAll("span");
        while (n.length < cells.length) n = "0" + n;
        n = n.slice(-cells.length);
        for (var i = 0; i < cells.length; i++) cells[i].textContent = n.charAt(i);
      })
      .catch(function () {});
  }
})();
