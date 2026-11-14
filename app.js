import { t } from "./core/i18n.js";
import { registerModule, listModules } from "./core/registry.js";

registerModule({ id: "basic-calculations", tier: "free", titleKey: "basicCalculations" });

function renderMenu() {
  let root = document.getElementById("menu");
  if (!root) {
    root = document.createElement("main");
    root.id = "menu";
    document.body.prepend(root);
  }
  root.innerHTML = "";

  const title = document.createElement("h1");
  title.textContent = t("appName");
  root.appendChild(title);

  const tagline = document.createElement("p");
  tagline.textContent = t("tagline");
  root.appendChild(tagline);

  for (const m of listModules()) {
    const btn = document.createElement("button");
    btn.className = "module-btn";
    btn.textContent = `${t(m.titleKey)} (${t(m.tier)})`;
    btn.onclick = () => console.log("open module", m.id);
    root.appendChild(btn);
  }
}

renderMenu();
