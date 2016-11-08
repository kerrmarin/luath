'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var autoprefixer = require('autoprefixer');

var paths = {
    scripts: ['_assets/**/*.js'],
    styles: ['_assets/**/*.scss']
};

//Minify all CSS files
gulp.task('minify-css', function() {
  return gulp.src(paths.styles)
    .pipe($.sass().on('error', $.sass.logError))
    .pipe($.postcss([ autoprefixer({ browsers: ['last 2 version'] }) ]))
    .pipe($.cleanCss())
    .pipe(gulp.dest('../static'))
    .pipe($.filesize());
});

//Watch the SCSS folder
gulp.task('watch', function () {
    gulp.watch(paths.styles, ['minify-css']);
});

//Minify task
gulp.task('minify', ['minify-css'])
//Default task
gulp.task('default', ['minify']);
