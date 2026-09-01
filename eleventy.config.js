export default function (eleventyConfig) {
  // Pass static assets straight through.
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  // Custom-domain cutover: create src/CNAME containing `dariocannizzaro.com`,
  // then uncomment the line below. See README "Going live on the real domain".
  // eleventyConfig.addPassthroughCopy("src/CNAME");

  // Essays, newest first.
  eleventyConfig.addCollection("writing", (api) =>
    api.getFilteredByTag("writing").sort((a, b) => b.date - a.date)
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
