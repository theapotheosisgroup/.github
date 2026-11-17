import assert from "node:assert/strict";
import { test } from "node:test";
import * as api from "../src/greet.mjs";

test("the module exports exactly the documented surface", () => {
  assert.deepEqual(Object.keys(api).sort(), ["greet"]);
  assert.equal(api.greet.length, 1);
});
