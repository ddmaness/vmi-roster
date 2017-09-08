//include gulp
var gulp = require('gulp');
//include karma
var Server = require('karma').Server;

//run test once and exit
gulp.task('test',function(){
    new Server({
        configFile: __dirname + '/my.conf.js',
        singleRun: true
    }, done).start();
});

//Watch for file changes and re-run tests on each change
gulp.task('tdd', function (done) {
  new Server({
    configFile: __dirname + '/my.conf.js'
  }, done).start();
});

gulp.task('default', ['tdd']);

// include plugins
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');

//lint task
gulp.task('lint', function(){
    return gulp.src('js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

//Concatenate and minify JS
gulp.task('scripts', function(){
    return gulp.src('js/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('dist'))
        .pipe(rename(all.min.js))
        .pipe(uglify())
        .pipe(gulp.dest('dist/js'));
});

//watch files for changes
gulp.task('watch',function(){
    gulp.watch('js/*.js', ['lint', 'scripts']);
});

//default task
gulp.task('default', ['lint', 'scripts', 'watch']);
