// NetPulse website behaviour (no dependencies):
// - Download page: OS tabs, preselecting the visitor's operating system.
// - Content tabs labelled Windows / macOS / Linux anywhere on the site: same preselection.
// - "Copy" buttons for checksums.
// - Home: "Download for <your OS>".
(function () {
  function detectOS() {
    var p = ((navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || navigator.userAgent || "").toLowerCase();
    if (p.indexOf("mac") !== -1 || p.indexOf("iphone") !== -1 || p.indexOf("ipad") !== -1) return "macOS";
    if (p.indexOf("linux") !== -1 || p.indexOf("x11") !== -1 || p.indexOf("cros") !== -1) return "Linux";
    return "Windows";
  }

  function selectOS(root, os) {
    root.querySelectorAll("[data-np-os]").forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.npOs === os)); });
    root.querySelectorAll("[data-np-panel]").forEach(function (p) { p.hidden = p.dataset.npPanel !== os; });
  }

  function init() {
    var os = detectOS();
    var hash = (location.hash || "").replace("#", "").toLowerCase();
    var fromHash = { windows: "Windows", macos: "macOS", linux: "Linux" }[hash];

    document.querySelectorAll(".np-ostabs-root").forEach(function (root) {
      root.querySelectorAll("[data-np-os]").forEach(function (b) {
        if (b.dataset.npOs === os) b.insertAdjacentHTML("beforeend", ' <span class="np-detected">your system</span>');
        b.addEventListener("click", function () { selectOS(root, b.dataset.npOs); history.replaceState(null, "", "#" + b.dataset.npOs.toLowerCase()); });
      });
      selectOS(root, fromHash || os);
    });

    // Markdown content tabs (pymdownx.tabbed) labelled with an OS name
    document.querySelectorAll(".tabbed-set").forEach(function (set) {
      var labels = set.querySelectorAll(":scope > .tabbed-labels > label");
      labels.forEach(function (label) {
        if (label.textContent.trim().indexOf(os) === 0) {
          var input = document.getElementById(label.getAttribute("for"));
          if (input) input.checked = true;
        }
      });
    });

    document.querySelectorAll("[data-np-download-os]").forEach(function (a) {
      a.textContent = "Download for " + os;
      a.href = a.getAttribute("href").split("#")[0] + "#" + os.toLowerCase();
    });

    document.querySelectorAll("[data-np-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = "Copy"; }, 1500); };
        if (navigator.clipboard) navigator.clipboard.writeText(btn.dataset.npCopy).then(done, function () {});
      });
    });
  }

  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
