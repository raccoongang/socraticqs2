function Logging(){
  var stream = through.obj(function (file, enc, callback) {
    console.log("stream:");
    console.log(file, enc, callback);
    this.push(file);
    return callback();
  });

  return stream;
}

var gulp = require('gulp'),
    stylus = require('gulp-stylus'), 
    csso = require('gulp-csso'), 
    uglify = require('gulp-uglify'), 
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    autoprefixer = require('gulp-autoprefixer'),
    order = require("gulp-order"),
    rjs = require('gulp-requirejs');
var through = require('through2');



//  JS
gulp.task('js-move', function() {
   return gulp.src(['./mysite/assets/js/lib/*.js', './mysite/assets/js/src/*.js', '!./mysite/assets/js/lib/require.js'])
       //.pipe(concat('main.min.js'))
       .pipe(uglify())
       .on('error', console.log)
       .pipe(gulp.dest('./mysite/mysite/static/js/'));

});

gulp.task('js', function() {
   return gulp.src([
       '!./mysite/assets/js/src/config.js',
       '!./mysite/assets/js/lib/require.js',
       '!./mysite/assets/js/lib/backbone.js',
       './mysite/assets/js/lib/*.js',
       './mysite/assets/js/src/*.js'])
       .pipe(order([
            "jquery-2.1.1.min.js",
            "*.js",

          ]))
       .pipe(concat('main.min.js'))
      // .pipe(uglify())
       .on('error', console.log)
       .pipe(gulp.dest('./mysite/mysite/static/js/'));

});

gulp.task('js-require', function() {
   return gulp.src(['./mysite/assets/js/lib/require.js', './mysite/assets/js/src/require.js'])
       .pipe(uglify())
       .on('error', console.log)
       .pipe(gulp.dest('./mysite/mysite/static/js/lib'));

});

gulp.task('require-config', function() {
   return gulp.src(['./mysite/assets/js/src/config.js'])
       .pipe(uglify())
       .on('error', console.log)
       .pipe(gulp.dest('./mysite/mysite/static/js'));

});

// CSS
gulp.task('css', function() {
    return gulp.src(['./mysite/assets/css/src/*.css', './mysite/assets/css/lib/*.css'])
        //.pipe(minifyCSS())
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9'))
        .pipe(concat('main.css'))
        .pipe(gulp.dest('./mysite/mysite/static/css/'));
});


gulp.task('rbuild', function() {
    rjs({
        baseUrl: './mysite/assets/js/src/file.js',
        out: './mysite/mysite/static/js/',
        shim: {
            underscore: {
                exports: '_'
            },
            backbone: {
                deps: [
                    'underscore',
                    'jquery'
                ],
                exports: 'Backbone'
            },
            'backbone-relational': {
                deps: [
                    'backbone'
                ],
                exports: 'RelationalModel'
            }
        },
    })
        .pipe(gulp.dest('./delpoy/'));
});

gulp.task('default', ['js', 'js-require', 'require-config', 'css', ]);