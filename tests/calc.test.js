import assert from "node:assert/strict";
import { spindleTorque, hydraulicForce, spindleSpeed, feedRate } from "../modules/basic-calculations/calc.js";

const near = (a, b, eps = 0.001) => assert.ok(Math.abs(a - b) < eps, `${a} ≠ ${b}`);

near(spindleTorque(7.5, 3000), 23.875);
near(hydraulicForce(100, 50), 19.635);
near(spindleSpeed(100, 50), 636.620, 0.01);
near(feedRate(1000, 4, 0.1), 400);

console.log("All calculation tests passed.");
