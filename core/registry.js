const modules = new Map();

export function registerModule(meta) {
  if (!meta || !meta.id) throw new Error("Module must have an id");
  if (modules.has(meta.id)) throw new Error(`Duplicate module: ${meta.id}`);
  modules.set(meta.id, meta);
}

export function getModule(id) {
  return modules.get(id);
}

export function listModules({ tier } = {}) {
  const all = [...modules.values()];
  return tier ? all.filter(m => m.tier === tier) : all;
}
