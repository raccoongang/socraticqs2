var watch = require('gulp-watch');
var batch = require('gulp-batch');

function Logging() {
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
gulp.task('js-move', function () {
    return gulp.src(['./mysite/assets/js/lib/*.js', './mysite/assets/js/src/*.js', '!./mysite/assets/js/lib/require.js'])
        //.pipe(concat('main.min.js'))
        .pipe(uglify())
        .on('error', console.log)
        .pipe(gulp.dest('./mysite/assets/static/js/'));

});

gulp.task('copy_structure', function () {
    gulp.src([
            './mysite/assets/js/src/**/*',
            '!./mysite/assets/js/src/config.js',
            '!./mysite/assets/js/src/ct.js',
            '!./mysite/assets/js/src/issue.js'
        ])
        .pipe(gulp.dest('./mysite/assets/static/js/'));
});

gulp.task('js', function () {
    return gulp.src(['.mysite/../node_modules/jquery/dist/jquery.min.js',
            '.mysite/../node_modules/bootstrap/dist/js/bootstrap.min.js',])
        .pipe(order([
            "jquery*.min.js",
            "*.js",

        ]))
        .pipe(concat('main.min.js'))
        .pipe(uglify())
        .on('error', console.log)
        .pipe(gulp.dest('./mysite/assets/static/js/'));

});

gulp.task('js-require', function () {
    return gulp.src(['.mysite/../node_modules/requirejs/require.js'])
        .pipe(uglify())
        .on('error', console.log)
        .pipe(gulp.dest('./mysite/assets/static/js/lib'));

});


// CSS
gulp.task('css', function () {
    return gulp.src(['./mysite/assets/css/src/*.css', './mysite/assets/css/lib/*.css'])
        //.pipe(minifyCSS())
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9'))
        .pipe(concat('main.css'))
        .pipe(gulp.dest('./mysite/assets/static/css/'));
});


gulp.task('rbuild', function () {
    rjs({
        name: "config",
        baseUrl: './mysite/assets/js/src/',
        out: 'app.js',
        delimiter: '\t',
        paths: {
            jquery: '../../../../node_modules/jquery/dist/jquery',
            underscore: '../../../../node_modules/underscore/underscore',
            backbone: '../../../../node_modules/backbone/backbone',
            text: '../../../../node_modules/requirejs-text/text',
            bootstrap: '../../../../node_modules/bootstrap/dist/js/bootstrap',
            mathjax: "../../../../node_modules/mathjax/MathJax"
        },
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
            backboneLocalstorage: {
                deps: ['backbone',],
                exports: 'Store'
            },
            bootstrap: {deps: ['jquery']},
            mathjax: {
                exports: "MathJax",
                init: function () {
                    MathJax.Hub.Startup.onload();
                    return MathJax;
                }
            }
        },
    })
    //.pipe(uglify())
        .pipe(gulp.dest('./mysite/assets/static/js/'));
});

gulp.task('watch', function () {
    watch([
        './mysite/assets/js/src/**/*',
        '!./mysite/assets/js/src/issue.js'
    ], batch(function (events, done) {
        gulp.start('rbuild', done);
    }));
});

gulp.task('default', ['js-require', 'rbuild', 'js', 'css']);
