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

  // Essays, newest first.
  eleventyConfig.addCollection("writing", (api) =>
    api.getFilteredByTag("writing").sort((a, b) => b.date - a.date)
  );

  // Resonance before recency: essays with `featured: true` in their front
  // matter surface in the "Start here" cluster above the full index.
  eleventyConfig.addCollection("writingFeatured", (api) =>
    api
      .getFilteredByTag("writing")
      .filter((p) => p.data.featured)
      .sort((a, b) => b.date - a.date)
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
