'use strict';

const gulp = require("gulp"),
    sass = require("gulp-sass"),
    clean = require('gulp-clean');

// set paths ...
const config = {
	scssPath: "src/scss",
	destPath: "application/static/stylesheets",
  assetPath: "application/static/govuk-frontend/assets",
  imgDestPath: "application/static/govuk_template/images"
}

// Tasks used to generate latest stylesheets
// =========================================
const cleanCSS = () => 
  gulp
    .src('application/static/stylesheets/**/*', {read: false})
    .pipe(clean());
cleanCSS.description = `Delete old stylesheets files`;

// compile scss to CSS
const compileStylesheets = () =>
  gulp
    .src( config.scssPath + '/*.scss')
	  .pipe(sass({outputStyle: 'expanded',
		  includePaths: [ 'src/scss', 'src/govuk-frontend']}))
      .on('error', sass.logError)
    .pipe(gulp.dest(config.destPath));

// Tasks for copying assets to application
// ======================================
const copyGovukStylesheets = () =>
  gulp
    .src('src/govuk/stylesheets/*')
    .pipe(gulp.dest(config.destPath + "/govuk"));

const copyGovukAssets = () => 
  gulp
    .src('src/govuk-frontend/assets/**/*')
    .pipe(gulp.dest(config.assetPath));

// Tasks to expose to CLI
// ======================
const latestStylesheets = gulp.series(
  cleanCSS,
  compileStylesheets,
  gulp.parallel(
    copyGovukStylesheets,
    copyGovukAssets
  )
);
latestStylesheets.description = `Generate the latest stylesheets`;

// Watch for scss changes
const watch = () => gulp.watch("src/scss/**/*", latestStylesheets);
watch.description = `Watch all project .scss for changes, then rebuild stylesheets.`;

// Set watch as default task
exports.default = watch;
exports.stylesheets = latestStylesheets;