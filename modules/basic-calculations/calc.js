// n = 1000 · Vc / (π · D)   [Vc: m/min, D: mm, n: rpm]
export function spindleSpeed(vc, d) {
  return (1000 * vc) / (Math.PI * d);
}

// Vf = n · z · fz   [mm/min]
export function feedRate(n, z, fz) {
  return n * z * fz;
}

// T = 9550 · P / n   [N·m]
export function spindleTorque(powerKw, rpm) {
  return (9550 * powerKw) / rpm;
}

// F(kN) = P · π · D² / 40000
export function hydraulicForce(pressureBar, diameterMm) {
  return (pressureBar * Math.PI * diameterMm * diameterMm) / 40000;
}
