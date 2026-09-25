// Shared: theme toggle. Storage is a convenience only; every read/write is guarded.
(function () {
  var root = document.documentElement;
  function get() { try { return localStorage.getItem("theme"); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem("theme", v); } catch (e) {} }
  var saved = get();
  if (saved) root.setAttribute("data-theme", saved);
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".theme");
    if (!b) return;
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme:dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next); set(next);
  });
})();
