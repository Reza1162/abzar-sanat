const KEY = "manatek.license";

export function getAccessLevel() {
  return localStorage.getItem(KEY) === "pro" ? "pro" : "free";
}

export function grantPro() {
  localStorage.setItem(KEY, "pro");
}

export function revokePro() {
  localStorage.removeItem(KEY);
}
