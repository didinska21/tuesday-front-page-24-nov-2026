// Entry point for the news-image-20261124 submission.
// Node 22, standard library only: copies the bundled front page
// (entry.png, drawn by draw_frontpage.py) to /output/entry.png.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = "/output";
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
console.log(`copied ${source} -> ${dest}`);
