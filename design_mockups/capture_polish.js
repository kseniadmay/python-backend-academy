const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1600, deviceScaleFactor: 2 });
  await page.goto("file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/design_mockups/echelon_readiness_polish.html", { waitUntil: "networkidle0" });

  const outDir = "C:/Users/fury6/.gemini/antigravity/brain/d689245c-f3a9-498f-b883-ee4a97e4b9bc";
  const cards = await page.$$(".variant-card");
  const names = ["echelon_polish_vA", "echelon_polish_vB", "echelon_polish_vC"];
  for (let i = 0; i < cards.length; i++) {
    await cards[i].screenshot({ path: path.join(outDir, `${names[i]}.png`) });
  }
  await page.screenshot({ path: path.join(outDir, "echelon_polish_all.png"), fullPage: true });
  await browser.close();
  console.log("All screenshots captured successfully!");
})();
