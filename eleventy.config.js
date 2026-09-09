export default function (eleventyConfig) {
  // Pass static assets straight through.
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  // Custom-domain cutover: create src/CNAME containing `dariocannizzaro.com`,
  // then uncomment the line below. See README "Going live on the real domain".
  // eleventyConfig.addPassthroughCopy("src/CNAME");

  // True while running `npm start` (serve/watch), false for `npm run build`.
  // Scaffolding that helps Dario see the shape of a page — [logline pending]
  // and friends — is gated on this so it can never reach a producer.
  eleventyConfig.addGlobalData("isDev", process.env.ELEVENTY_RUN_MODE !== "build");

  // The front page's LAST UPDATED stamp is the build time — every deploy is a
  // real update, so the stamp is honest by construction. DD.MM.YYYY, 2004-style.
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  eleventyConfig.addGlobalData(
    "buildDate",
    `${pad(now.getUTCDate())}.${pad(now.getUTCMonth() + 1)}.${now.getUTCFullYear()}`
  );
  eleventyConfig.addGlobalData("buildYear", String(now.getUTCFullYear()));

  // Everything in src/writing/, newest first.
  const byDate = (a, b) => b.date - a.date;
  eleventyConfig.addCollection("writing", (api) =>
    api.getFilteredByTag("writing").sort(byDate)
  );

  // The two shelves of READ SOMETHING. `kind: story` or `kind: essay` in a file's
  // front matter decides which; a file with neither still lands in `writing`.
  eleventyConfig.addCollection("stories", (api) =>
    api.getFilteredByTag("writing").filter((p) => p.data.kind === "story").sort(byDate)
  );
  eleventyConfig.addCollection("essays", (api) =>
    api.getFilteredByTag("writing").filter((p) => p.data.kind === "essay").sort(byDate)
  );

  // POEMS. Ordered by hand (`order` in front matter), because a poem's date is
  // often a guess and the sequence on the page is a choice, not a timestamp.
  eleventyConfig.addCollection("poems", (api) =>
    api.getFilteredByTag("poems").sort((a, b) => (a.data.order || 99) - (b.data.order || 99))
  );

  // 12 September 2026
  eleventyConfig.addFilter("longDate", (d) =>
    new Intl.DateTimeFormat("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
      timeZone: "UTC",
    }).format(d)
  );

  // 2026-09-12, for <time datetime="">
  eleventyConfig.addFilter("isoDate", (d) => d.toISOString().slice(0, 10));

  // 2026 — the READ SOMETHING index shows years only; the piece itself shows the day.
  eleventyConfig.addFilter("year", (d) => String(d.getUTCFullYear()));

  return {
    pathPrefix: process.env.PATH_PREFIX || "/",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
