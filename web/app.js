(() => {
  "use strict";

  const canvas = document.getElementById("preview");
  const ctx = canvas.getContext("2d", { alpha: false });
  const materialInput = document.getElementById("material");
  const resolutionInput = document.getElementById("resolution");
  const generateButton = document.getElementById("generate");
  const exportButton = document.getElementById("export");
  const status = document.getElementById("status");
  const emptyState = document.getElementById("empty-state");
  const sizeLabel = document.getElementById("preview-size");
  let hasTexture = false;
  let generation = 0;

  const clamp = (v, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, v));
  const smooth = t => t * t * (3 - 2 * t);

  function randomGrid(cells, seed) {
    const grid = new Float32Array((cells + 1) * (cells + 1));
    let state = seed >>> 0;
    for (let i = 0; i < grid.length; i++) {
      state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
      grid[i] = state / 4294967296;
    }
    return grid;
  }

  function noiseAt(x, y, cells, grid) {
    const gx = x * cells, gy = y * cells;
    const x0 = Math.floor(gx), y0 = Math.floor(gy);
    const tx = smooth(gx - x0), ty = smooth(gy - y0);
    const stride = cells + 1;
    const a = grid[y0 * stride + x0], b = grid[y0 * stride + x0 + 1];
    const c = grid[(y0 + 1) * stride + x0], d = grid[(y0 + 1) * stride + x0 + 1];
    const top = a + (b - a) * tx, bottom = c + (d - c) * tx;
    return top + (bottom - top) * ty;
  }

  function generate() {
    const size = Number(resolutionInput.value);
    const scale = Number(document.getElementById("scale").value);
    const noise = Number(document.getElementById("noise").value);
    const detail = Number(document.getElementById("detail").value);
    const material = materialInput.value;
    const seed = (Date.now() + (++generation * 2654435761)) >>> 0;
    const coarseCells = Math.max(3, Math.floor(5 + scale * 30));
    const fineCells = Math.max(12, Math.floor(24 + detail * 120));
    const coarseGrid = randomGrid(coarseCells, seed);
    const fineGrid = randomGrid(fineCells, seed ^ 0x9e3779b9);
    const grainGrid = randomGrid(64, seed ^ 0x85ebca6b);
    const pixels = ctx.createImageData(size, size);
    const data = pixels.data;

    generateButton.disabled = true;
    generateButton.textContent = "Generating…";
    status.textContent = "Generating texture…";

    // Yield once so the interface can display the generating state.
    setTimeout(() => {
      let p = 0;
      for (let y = 0; y < size; y++) {
        const ny = y / size;
        for (let x = 0; x < size; x++) {
          const nx = x / size;
          const coarse = noiseAt(nx, ny, coarseCells, coarseGrid);
          const fine = noiseAt(nx, ny, fineCells, fineGrid);
          const grain = noiseAt(nx, ny, 64, grainGrid);
          let field = coarse * (0.72 - detail * 0.18) + fine * (0.18 + detail * 0.28);
          field += grain * (0.08 + noise * 0.28);
          field = clamp((field - 0.5) * (0.9 + noise * 1.5) + 0.5);
          let r, g, b, value;

          if (material === "concrete") {
            value = 0.34 + field * 0.30;
            const pore = grain > (0.992 - detail * 0.012) ? (0.12 + detail * 0.12) : 0;
            value = clamp(value - pore);
            r = value * 0.94; g = value * 0.97; b = value;
          } else if (material === "wood") {
            const wave = Math.sin((nx * (8 + scale * 34) + coarse * (1.4 + detail * 3)) * 2 * Math.PI);
            value = clamp(0.30 + (wave * 0.5 + 0.5) * 0.36 + (fine - 0.5) * noise * 0.22);
            r = value; g = value * 0.66; b = value * 0.38;
          } else if (material === "metal") {
            const brushed = Math.sin((ny * (35 + scale * 110) + fine * detail * 2) * 2 * Math.PI);
            value = clamp(0.36 + field * 0.28 + brushed * (0.025 + detail * 0.035));
            if (grain > (0.997 - detail * 0.008)) value = clamp(value - 0.22);
            r = value * 0.84; g = value * 0.90; b = value;
          } else {
            const frequency = 5 + Math.floor(scale * 13);
            const pattern = Math.sin(nx * frequency * 2 * Math.PI) * Math.sin(ny * frequency * 2 * Math.PI) * 0.5 + 0.5;
            value = clamp(0.58 + pattern * 0.22 + (field - 0.5) * noise * 0.18);
            r = value; g = value * 0.88; b = value * 0.65;
          }

          data[p++] = Math.round(clamp(r) * 255);
          data[p++] = Math.round(clamp(g) * 255);
          data[p++] = Math.round(clamp(b) * 255);
          data[p++] = 255;
        }
      }

      canvas.width = size;
      canvas.height = size;
      ctx.putImageData(pixels, 0, 0);
      canvas.style.display = "block";
      emptyState.hidden = true;
      hasTexture = true;
      exportButton.disabled = false;
      sizeLabel.textContent = size + " × " + size;
      status.textContent = material[0].toUpperCase() + material.slice(1) + " · " + size + " × " + size + " · Generated";
      generateButton.disabled = false;
      generateButton.innerHTML = "<span>✦</span> Generate texture";
    }, 20);
  }

  function exportPNG() {
    if (!hasTexture) return;
    const link = document.createElement("a");
    link.download = "texture-valley-" + materialInput.value + "-" + canvas.width + "x" + canvas.height + ".png";
    link.href = canvas.toDataURL("image/png");
    link.click();
    status.textContent = "PNG exported · " + link.download;
  }

  ["scale", "noise", "detail"].forEach(id => {
    const input = document.getElementById(id);
    const output = document.getElementById(id + "-value");
    input.addEventListener("input", () => { output.value = Number(input.value).toFixed(2); });
  });

  generateButton.addEventListener("click", generate);
  exportButton.addEventListener("click", exportPNG);
  resolutionInput.addEventListener("change", () => {
    sizeLabel.textContent = resolutionInput.value + " × " + resolutionInput.value;
  });

  generate();
})();