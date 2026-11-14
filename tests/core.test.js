import assert from "node:assert/strict";
import { t, setLang } from "../core/i18n.js";
import { registerModule, getModule, listModules } from "../core/registry.js";

setLang("en");
assert.equal(t("appName"), "ManaTek");
setLang("fa");
assert.equal(t("appName"), "ManaTek");
assert.equal(t("missing.key"), "missing.key");

registerModule({ id: "basic-calculations", tier: "free" });
assert.equal(getModule("basic-calculations").tier, "free");
assert.equal(listModules({ tier: "free" }).length, 1);
assert.throws(() => registerModule({ id: "basic-calculations" }));

console.log("Core tests passed.");
